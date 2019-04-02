"""
Copyright (c) 2019, NVIDIA CORPORATION. All rights reserved.

NVIDIA CORPORATION and its licensors retain all intellectual property
and proprietary rights in and to this software, related documentation
and any modifications thereto. Any use, reproduction, disclosure or
distribution of this software and related documentation without an express
license agreement from NVIDIA CORPORATION is strictly prohibited.
"""

load("//engine/build:isaac.bzl", "isaac_app")
load("//engine/build:isaac.bzl", "isaac_cc_module", "isaac_doc_dep")

isaac_doc_dep(
    name = "doc",
    srcs = [
        "NavigationRosBridge.cpp",
        "NavigationRosBridge.hpp",
        "doc/ros.rst",
    ],
    visibility = ["//visibility:public"],
)

isaac_cc_module(
    name = "navigation_ros_bridge",
    srcs = [
        "NavigationRosBridge.cpp",
    ],
    hdrs =
        ["NavigationRosBridge.hpp"],
    tags = [
        "manual",
    ],
    visibility = ["//visibility:public"],
    deps = [
        "//engine/alice",
        "//engine/core",
        "//engine/core/image",
        "//engine/core/math",
        "//engine/core/tensor",
        "//engine/gems/sight",
        "//messages",
        "//third_party:ros",
    ],
)

isaac_app(
    name = "navigation_rosbridge",
    app_json_file = "navigation_rosbridge.app.json",
    modules = [
        "//apps/samples/navigation_rosbridge:navigation_ros_bridge",
    ],
    tags = ["manual"],
)
