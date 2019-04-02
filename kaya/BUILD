"""
Copyright (c) 2019, NVIDIA CORPORATION. All rights reserved.

NVIDIA CORPORATION and its licensors retain all intellectual property
and proprietary rights in and to this software, related documentation
and any modifications thereto. Any use, reproduction, disclosure or
distribution of this software and related documentation without an express
license agreement from NVIDIA CORPORATION is strictly prohibited.
"""

load("//engine/build:isaac.bzl", "isaac_app")

isaac_app(
    name = "joystick",
    data = [
        "//apps/kaya/robots",
    ],
    modules = [
        "kaya_base",
        "navigation",
        "sensors:joystick",
    ],
)

isaac_app(
    name = "object_detection",
    data = [
        "//apps/assets/maps",
        "//apps/kaya/robots",
        "@yolo_tensorrt_test_data_gtc2019_demo",
    ],
    modules = [
        "kaya_base",
        "ml",
        "navigation",
        "realsense",
        "sensors:joystick",
        "viewers",
        "yolo",
    ],
)

isaac_app(
    name = "follow_me",
    data = [
        "//apps/kaya/robots",
    ],
    modules = [
        "imu",
        "kaya_base",
        "navigation",
        "perception:april_tags",
        "perception",
        "planner",
        "realsense",
        "sensors:joystick",
        "viewers",
    ],
)

isaac_app(
    name = "gmapping_distributed_host",
    modules = [
        "navigation",
    ],
)

isaac_app(
    name = "gmapping_distributed_kaya",
    data = [
        "//apps/kaya/robots",
    ],
    modules = [
        "imu",
        "kaya_base",
        "navigation",
        "perception",
        "planner",
        "realsense",
        "sensors:joystick",
        "viewers",
    ],
)
