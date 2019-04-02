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
    name = "proportional_control_cpp_codelet",
    srcs = ["ProportionalControlCpp.cpp"],
    hdrs = ["ProportionalControlCpp.hpp"],
    visibility = ["//visibility:public"],
    deps = [
        "//engine/alice",
        "//engine/gems/state:io",
        "//messages",
        "//messages/state:differential_base",
    ],
)

isaac_app(
    name = "proportional_control_cpp",
    app_json_file = "proportional_control_cpp.app.json",
    modules = [
        "//apps/tutorials/proportional_control_cpp:proportional_control_cpp_codelet",
        "navigation",
        "segway",
        "sensors:joystick",
        "viewers",
    ],
)
