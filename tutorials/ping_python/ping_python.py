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
# For comparison, please see the same logic in C++ at "PingCpp.cpp".
#
# We receive odometry information, from which we extract the x position. Then, using refence and
# gain parameters that are provided by the user, we compute and publish a linear speed command
# using `control = gain * (reference - position)`
class PingPython(Codelet):
    def start(self):
        # This part will be run once in the beginning of the program

        # Message to be printed at every tick
        self.set_isaac_param("message", "Hello Word!")

        # We can tick periodically, on every message, or blocking. See documentation for details.
        self.tick_periodically(1.0)

    def tick(self):
        # This part will be run at every tick. We are ticking periodically in this example.

        # Print out message to console
        print(self.get_isaac_param("message"))


def main():
    app = Application(name="ping_python", modules=[])
    app.load_graph("apps/tutorials/ping_python/ping_python.graph.json")
    app.register({"ping_node": PingPython})
    app.start_webserver()
    app.start_wait_stop()


if __name__ == '__main__':
    main()
