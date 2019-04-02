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
    name = "link",
    app_json_file = "link.app.json",
    data = [
        "//apps/assets/maps",
    ],
    modules = [
        "communications",
        "imu",
        "navigation",
        "perception",
        "planner",
        "segway",
        "sensors:joystick",
        "stereo_depth:coarse_to_fine",
        "velodyne",
        "viewers",
        "zed",
    ],
)
