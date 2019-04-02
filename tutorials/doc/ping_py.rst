Developing Codelets in Python
=============================

While in terms of performance, the best language for writing codelets is C++, not all codelets of an
application need to be in the same language. The Isaac SDK also supports Python codelets, or
pyCodelets, for those who are more faimilar with Python.

This section shows you how to do the following:

- Run Python codelets, using `ping_python` included in the Isaac SDK as an example
- Create Python codelets

This section also describes the run script deployed with Python codelets to the target system, and
the differences between JSON and Bazel BUILD files for C++ codelets and JSON and Bazel BUILD files
for Python codelets.

Running a Python Codelet
^^^^^^^^^^^^^^^^^^^^^^^^

A Python version of the Ping codelet described in the :ref:`ping_cpp` section can be found in
the `apps/tutorials/ping_python/` directory.

This application can be run on your system by executing the following command:

.. code-block:: bash

   bob@desktop:~/isaac$ bazel run //apps/tutorials/ping_python

If you want to run the application on a Jetson device you can have to follow these instructions

1) Deploy the :samp:`ping_python-pkg` to the target machine with the following command:

  .. code-block:: bash

    bob@desktop:~/isaac$ ./engine/build/deploy.sh -p //apps/tutorials/ping_python:ping_python-pkg -h <target_ip> -d <device_type>

  See the :ref:`deployment_device` section for more details on deployment.

2) Change to the directory of the deployed package on Jetson with the following command:

   .. code-block:: bash

      bob@desktop:~/$ cd ~/deploy/bob/ping_python-pkg

      Where "bob" is your username on the host system.

3) If you have not yet installed pycapnp, install it with the following command:

   .. code-block:: bash

      bob@desktop:~/deploy/bob/ping_python-pkg/$ sudo apt install python-pip
      bob@desktop:~/deploy/bob/ping_python-pkg/$ python -m pip install pycapnp --user

   This may take about five minutes to complete, but once pycapnp is installed it does not need to be
   installed again. If this step is omitted or forgotten the error "ImportError: No module named
   capnp" is displayed.

4) Run the application by executing the following command:

   .. code-block:: bash

     bob@desktop:~/deploy/bob/ping_python-pkg/$ ./run apps/tutorials/ping_python/ping_python.py

When you run the codelet, by either method, a "Hello World!" message is printed every 1.5 seconds.
Modify the script at `apps/tutorials/ping_python/ping_python.py` and run it again to see the effects
of your changes.

A more complete example, the Python version of the Proportional Control codelet described in the
:ref:`p_control_cpp` section is shown below. The following Python script is functionally equivalent
to a combination of `main.cpp`, `ProportionalControlCpp.hpp`, and `ProportionalControlCpp.cpp`:


.. code-block:: python

  from __future__ import absolute_import, division, print_function

  from engine.pyalice import *
  import apps.tutorials.proportional_control_python

  # A Python codelet for proportional control
  # For comparison, please see the same logic in C++ at "ProportionalControlCpp.cpp".
  #
  # We receive odometry information, from which we extract the x position.
  # Then, using refence and gain parameters that are provided by the user,
  # we compute and publish a linear speed command using
  #   `control = gain * (reference - position)`
  class ProportionalControlPython(Codelet):
      def start(self):
          # This part will be run once in the beginning of the program

          # Input and output messages for the Codelet.
          # We'll make connections in the json file.
          self.rx = self.isaac_proto_rx("Odometry2Proto", "odometry")
          self.tx = self.isaac_proto_tx("StateProto", "cmd")

          # Parameters. We'll be able to modify them through Sight website.
          self.set_isaac_param("desired_position_meters", 1.0)
          self.set_isaac_param("gain", 1.0)

          # Print some information
          print("Please head to the Sight website at <IP>:<PORT> to see how I am doing.")
          print("<IP> is the Internet Protocol address where the app is running,")
          print("and <PORT> is set in the config file, typically to '3000'.")
          print("By default, local link is 'localhost:3000'.")

          # We can tick periodically, on every message, or blocking.
          # See documentation for details.
          self.tick_periodically(0.01)

      def tick(self):
          # This part will be run at every tick.
          # We are ticking periodically in this example.

          # Nothing to do if we haven't received odometry data yet
          if not self.rx.available():
              return

          # Read parameters that can be set through Sight webpage
          reference = self.get_isaac_param("desired_position_meters")
          gain = self.get_isaac_param("gain")

          # Read odometry message received
          position = self.rx.get_proto().odomTRobot.translation.x

          # Compute the control action
          control = gain * (reference - position)

          # Show some data in Sight
          self.show("reference (m)", reference)
          self.show("position (m)", position)
          self.show("control", control)
          self.show("gain", gain)

          # Publish control command
          tx_message = self.tx.init_proto()
          data = tx_message.init('data', 2)
          data[0] = control  # linear speed
          data[1] = 0.0  # This simple example sets zero angular speed
          self.tx.publish()

  def main():
      app = Application("proportional_control_python", ["navigation", "segway", "sensors:joystick"])
      app.load_graph(
          "apps/tutorials/proportional_control_python/proportional_control_python.graph.json")
      app.load_config(
          "apps/tutorials/proportional_control_python/proportional_control_python.config.json")
      app.register({"py_controller": ProportionalControlPython})
      app.start_wait_stop()

  if __name__ == '__main__':
      main()

Import statements in Python are analagous to preprocessor `#include` statements in C++. Like in
`ProportionalControlCpp.cpp`, the codelet is defined in `start` and `tick` functions. The Isaac
parameters `desired_position_meters` and `gain` are used, with values either configured in JSON
files or set through Sight at runtime.

At every tick, if an odometry message is received, the appropriate command is computed and published
for the robot. Some important data is displayed in Sight.

The main function simply loads the graph and configuration files before runing the application, the
way that `main.cpp` does in the C++ codelet.

Creating Python Codelets
^^^^^^^^^^^^^^^^^^^^^^^^

Follow a procedure similar to the following when creating your Python codelets.

Create a Workspace
------------------

1. Copy `apps/tutorials/proportional_control_python/` or another existing Python-based codelet to
   `apps/<your_app_name>` as a template or starting point.

   If you use the Porportional Control codelet unmodified for this tutorial, a Carter robot or
   equivalent is required. See :ref:`carter_hardware` for more information.

2. Rename the files to reflect the name of your codelet instead of the codelet you copied.

Create a Bazel BUILD File
-------------------------

1. In `apps/<your_app_name>/BUILD` copied in with the other files used as a starting point, replace
   all `proportional_control_python` strings with `<your_app_name>`.

2. Modify the `data` property in the `py_binary` rule depending on the C++ codelets you use.

   For example, if you were to omit or remove `//packages/segway` in
   `apps/tutorials/proportional_control_python/BUILD`, and run the codelet, the error `Component with
   typename 'isaac::SegwayRmpDriver' not registered` would be displayed, because the Proportional
   Control codelet (`proportional_control_python.graph.json`) uses the C++
   based segway codelet.

3. Since our application is located in apps and not apps/tutorials, remove the specification of
   `//apps/tutorials:py_init`, leaving `//apps:py_init` in place.

   If instead of moving the application up to apps, you move it to `apps/tutorials/tutorials_sub`,
   the BUILD file in `apps/tutorials/tutorials_sub` must specify `py_init` in all three directories,
   `//apps:py_init`, `//apps/tutorials:py_init`, and `//apps/tutorials/tutorials_sub:py_init`. Each
   directory would also need a copy of `__init__.py`.

Create a Python Codelet
-----------------------

1. In your `<your_app_name>.py`, replace `import apps.tutorials.proportional_control_python` with
   `import apps.<your_app_name>`.

2. Rename and modify the `ProportionalControlPython` class as needed. You can define multiple Python
   codelets in this file.

3. In the main function, replace all `proportional_control_python` strings with <your_app_name>. You
   must register all pyCodelets using their class names, such as ProportionalControlPython in the
   files we used as a starting point. Modify node names, `py_controller` in this case, to match the
   name you chose in your `graph.json` file.

   Your main function will be similar to the following:

  .. code-block:: python

    def main():
      app = Application("my_new_app")
      app.load_graph("apps/my_new_app/my_new_app.graph.json")
      app.load_config("apps/my_new_app/my_new_app.config.json")
      app.register({"my_py_node1": PyCodeletType1, "my_py_node2a": PyCodeletType2, "my_py_node2b": PyCodeletType2})
      app.start_wait_stop()

4. Add or remove nodes, components, or edges in `apps/<your_app_name>/<your_app_name>.graph.json`
   depending on your codelet.

5. Configure nodes and components in `apps/<your_app_name>/<your_app_name>.config.json` as needed.
   Make sure eto replace all instances of the codelet name with the name of your new codelet.

Run the codelet locally or deploy and run it on a Jetson system as described in `Running a
Python Codelet`_.

The run Script
^^^^^^^^^^^^^^

The run script, provided along with deployment (using deploy.sh) of an Isaac application that
includes a Python codelet or codelets, performs the following functions:

- Checks that the filename of the Python script ends in ".py"

- Verifies that every directory has an `__init__.py` file

- Runs the application using the following command.

  .. code-block:: bash

     PYTHONPATH=$PWD:$PWD/engine python

These functions are performed by the run script when we use the following command:

.. code-block:: bash

   ./run apps/tutorials/proportional_control_python/proportional_control_python.py

JSON and BUILD Files for Python Codelets
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

JSON files for Python codelets are very similar to those for C++ codelets, except that the component
type of Python codelets is always `isaac::alice::PyCodelet`.

Bazel BUILD files are somewhat different, as shown in the following example:

.. code-block:: none

    load("//engine/build:isaac.bzl", "isaac_pkg")

    py_binary(
        name = "proportional_control_python",
        srcs = [
            "__init__.py",
            "proportional_control_python.py",
        ],
        data = [
            "proportional_control_python.config.json",
            "proportional_control_python.graph.json",
            "//apps:py_init",
            "//apps/tutorials:py_init",
            "//messages:core_messages",
            "//packages/navigation:libnavigation_module.so",
            "//packages/segway:libsegway_module.so",
            "//packages/sensors:libjoystick_module.so",
        ],
        deps = ["//engine/pyalice"],
    )

    isaac_pkg(
        name = "proportional_control_python-pkg",
        srcs = ["proportional_control_python"],
    )

Use of C++ codelets is enabled by specifying the corresponding modules in `data` in the `py_binary`
rule. For example, `//packages/segway:libsegway_module.so` is required to use C++ Codelet of type
`isaac::SegwayRmpDriver`. Omitting or forgetting this dependency causes the error `Component with
typename 'isaac::SegwayRmpDriver' not registered` to be displayed when the application is run.

The `isaac_pkg` rule is responsible for packing all the files up and creating an archive which
can be transfered to the target device with the deploy script.
