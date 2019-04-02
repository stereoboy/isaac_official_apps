'''
Copyright (c) 2019, NVIDIA CORPORATION. All rights reserved.

NVIDIA CORPORATION and its licensors retain all intellectual property
and proprietary rights in and to this software, related documentation
and any modifications thereto. Any use, reproduction, disclosure or
distribution of this software and related documentation without an express
license agreement from NVIDIA CORPORATION is strictly prohibited.
'''
load("//engine/build:isaac.bzl", "isaac_app")

isaac_app(
    name = "follow_me",
    app_json_file = "follow_me.app.json",
    modules = [
        "navigation",
        "perception:april_tags",
        "perception",
        "planner",
        "segway",
        "realsense",
        "sensors:joystick",
        "velodyne",
        "viewers",
        "zed",
    ],
)
