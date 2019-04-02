'''
Copyright (c) 2019, NVIDIA CORPORATION. All rights reserved.

NVIDIA CORPORATION and its licensors retain all intellectual property
and proprietary rights in and to this software, related documentation
and any modifications thereto. Any use, reproduction, disclosure or
distribution of this software and related documentation without an express
license agreement from NVIDIA CORPORATION is strictly prohibited.
'''
load("//engine/build:isaac.bzl", "isaac_app", "isaac_cc_module")

isaac_cc_module(
    name = "watpoint_from_slack",
    srcs = ["WaypointFromSlack.cpp"],
    hdrs = ["WaypointFromSlack.hpp"],
    visibility = ["//visibility:public"],
    deps = [
        "//engine/alice",
        "//engine/gems/algorithm:string_utils",
        "//messages",
    ],
)

isaac_app(
    name = "slackbot",
    data = [
        "//apps/assets/maps",
        "//apps/carter/robots",
    ],
    modules = [
        "//apps/carter/slackbot:watpoint_from_slack",
        "communications",
        "map",
        "navigation",
        "perception",
        "planner",
        "segway",
        "sensors:joystick",
        "velodyne",
        "viewers",
    ],
)
