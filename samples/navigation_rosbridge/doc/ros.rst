ROS Bridge Overview and Workflow
=====================================
Both ROS and Isaac make use of message passing to handle communication
between different parts of their respective systems.
Communicating between ROS and Isaac requires creating a message translation
layer between the two systems.  The simplest method for doing so involves
turning an Isaac codelet into a full fledged ROS node. The majority of ROS
functionality is not required by Isaac, thus the included packages only offer
support for the messages commonly installed with a default ROS install. In order
to make use of custom ROS messages it is necessary to generate a custom package
and point the bazel build system to such a package.

The third-party libraries required for the ROS Bridge are only supported on desktop and Jetson
Xavier.

Install ROS
--------------------------------------

In order to use the ROS bridge you have to install ROS on your device. For example if you want to
use the ROS bridge on Jetson you have to install ROS on Jetson. If you want to use ROS on the
desktop you have to install ROS on the desktop.

The ROS version you install has to match the operating system of your device. For Ubuntu 16.04
you have to install ROS Kinetic Kame. On Jetson Xavier or Jetson Nano you have to install ROS
Melodic Morenia.

To install ROS follow the instructions from the `ROS webpage`_.

.. _ROS webpage: http://wiki.ros.org/ROS/Installation


Making a ROS Bridge Codelet
---------------------------------------
The following files demonstrate how to create a simple ROS-Isaac bridge codelet.
The code initializes or makes use of a ROS node during start, then on tick the ROS
message queues are pumped and the messages on both sides are translated and rebroadcast.
The following ROS packages are included by default in the shipped ROS package

.. code-block:: bash

    roscpp rospy actionlib_msgs control_msgs diagnostic_msgs geometry_msgs
    map_msgs nav_msgs pcl_msgs sensor_msgs shape_msgs std_msgs stereo_msgs
    tf2_geometry_msgs tf2_msgs trajectory_msgs visualization_msgs

NavigationRosBridge.hpp
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. literalinclude:: ../NavigationRosBridge.hpp
    :language: cpp


NavigationRosBridge.cpp
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. literalinclude:: ../NavigationRosBridge.cpp
    :language: cpp

Testing the ROS Bridge
-------------------------------------
In order to test a ROS Bridge codelet, it is necessary to create
a ROS test node.  The following code is a simple node used to test
the NavigationRosBridge discussed previously.

.. code-block:: cpp

    #include <ros/ros.h>
    // Include the appropriate message headers for your test case
    #include <geometry_msgs/Pose2D.h>

    // Sending random points for navigation testing
    #include <random>

    // A simple call back to acknowledge receiving a message
    void navigationCallback(const geometry_msgs::Pose2D::ConstPtr& msg) {
        ROS_INFO("Heard: Isaac is at X:%f, Y:%f, Theta: %f", msg->x, msg->y, msg->theta);
    }

    constexpr double pi = 3.14159265358979323846;

    int main(int argc, char **argv) {
        // Select a random point to send as a goal pose
        std::random_device rd;
        std::mt19937_64 eng(rd());
        std::uniform_real_distribution<> dist_x(10, 30);
        std::uniform_real_distribution<> dist_y(10, 30);
        std::uniform_real_distribution<> dist_theta(-pi, pi);

        ros::init(argc, argv, "rosBridgeTest");

        ros::NodeHandle rosBridgeTestNode;

        // Channel to publish navigation requests to.
        // Replace with desired message and channel name for your test case
        ros::Publisher nav_pub = rosBridgeTestNode.advertise<geometry_msgs::Pose2D>("isaac_navigation2D_request", 1000);

        // Listen for pose/navigation updates.
        // Replace with desired message and channel name for your test case
        ros::Subscriber nav_sub = rosBridgeTestNode.subscribe("isaac_navigation2D_status", 1000, navigationCallback);

        // Send a message and check updates every ten seconds
        ros::Rate loop_rate(10);

        while (ros::ok()) {
            // Generate a random goal location
            geometry_msgs::Pose2D pose_msg;
            pose_msg.x = dist_x(eng);
            pose_msg.y = dist_y(eng);
            pose_msg.theta = dist_theta(eng);

            ROS_INFO("Sent: Move Isaac to  X:%f, Y:%f, Theta: %f", pose_msg.x, pose_msg.y, pose_msg.theta);
            nav_pub.publish(pose_msg);

            // Manually spin to check messages
            ros::spinOnce();

            loop_rate.sleep();
        }
        return 0;
    }

Using a Custom ROS Package
----------------------------------------
To use a custom ROS package, you must first generate a custom workspace which contains
the required packages. Refer to **engine/build/scripts/ros_package_generation.sh** for guidelines
on how to create a custom package with the proper path structure. Once such a package exists,
modify **engine/build/workspace/ros.bzl** to point to the new workspace.

Begin by commenting out the platform specific default package, which should be similar
to the following:

.. code-block:: python

    isaac_new_http_archive(
        name = "isaac_ros_bridge_x86_64",
        build_file = clean_dep("//third_party:ros.BUILD"),
        sha256 = "b2a6c2373fe2f02f3896586fec0c11eea83dff432e65787f4fbc0ef82100070a",
        url = "https://developer.nvidia.com/isaac/download/third_party/ros_kinetic_x86_64.tar.gz",
    )

Replace the platform-specific package with the following to point to the new
workspace with the custom packages:

.. code-block:: python

    isaac_new_local_repository(
        name='isaac_ros_bridge_x86_64',
        path='path to the workspace',
        build_file = clean_dep("//third_party:ros.BUILD"),
    )

The name and build_file fields in the new section must match those of the
section being replaced.
