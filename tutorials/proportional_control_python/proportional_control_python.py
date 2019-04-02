'''
Copyright (c) 2019, NVIDIA CORPORATION. All rights reserved.

NVIDIA CORPORATION and its licensors retain all intellectual property
and proprietary rights in and to this software, related documentation
and any modifications thereto. Any use, reproduction, disclosure or
distribution of this software and related documentation without an express
license agreement from NVIDIA CORPORATION is strictly prohibited.
'''
from __future__ import absolute_import, division, print_function

from engine.pyalice import *

# A Python codelet for proportional control
# For comparison, please see the same logic in C++ at "ProportionalControlCpp.cpp".
#
# We receive odometry information, from which we extract the x position. Then, using refence and
# gain parameters that are provided by the user, we compute and publish a linear speed command
# using `control = gain * (reference - position)`
class ProportionalControlPython(Codelet):
    def start(self):
        # This part will be run once in the beginning of the program

        # Input and output messages for the Codelet. We'll make connections in the json file.
        self.rx = self.isaac_proto_rx("Odometry2Proto", "odometry")
        self.tx = self.isaac_proto_tx("StateProto", "cmd")  # DifferentialBaseControl type

        # Parameters. We'll be able to modify them through Sight website.
        self.set_isaac_param("desired_position_meters", 1.0)
        self.set_isaac_param("gain", 1.0)

        # Print some information
        print("Please head to the Sight website at <IP>:<PORT> to see how I am doing.")
        print("<IP> is the Internet Protocol address where the app is running,")
        print("and <PORT> is set in the config file, typically to '3000'.")
        print("By default, local link is 'localhost:3000'.")

        # We can tick periodically, on every message, or blocking. See documentation for details.
        self.tick_periodically(0.01)

    def tick(self):
        # This part will be run at every tick. We are ticking periodically in this example.

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
    app.start_webserver()
    app.start_wait_stop()

if __name__ == '__main__':
    main()
