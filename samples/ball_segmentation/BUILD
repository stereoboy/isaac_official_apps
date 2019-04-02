"""
Copyright (c) 2019, NVIDIA CORPORATION. All rights reserved.

NVIDIA CORPORATION and its licensors retain all intellectual property
and proprietary rights in and to this software, related documentation
and any modifications thereto. Any use, reproduction, disclosure or
distribution of this software and related documentation without an express
license agreement from NVIDIA CORPORATION is strictly prohibited.
"""

load("//engine/build:isaac.bzl", "isaac_app", "isaac_cc_library", "isaac_cc_module")

isaac_cc_module(
    name = "ball_segmentation_visualizer",
    srcs = ["VisualizePrediction.cpp"],
    hdrs = ["VisualizePrediction.hpp"],
    visibility = ["//visibility:public"],
    deps = [
        "//engine/alice",
        "//engine/gems/image",
        "//messages",
    ],
)

filegroup(
    name = "validation_dataset",
    srcs = glob([
        "ball_validation_dataset/**/*",
    ]),
)

py_binary(
    name = "training",
    srcs = ["training.py"],
    data = [
        ":training.config.json",
        ":training.graph.json",
        ":validation_dataset",
        "//packages/ml:libml_module.so",
        "//packages/perception:libperception_module.so",
        "//packages/viewers:libviewers_module.so",
    ],
    deps = [
        "//engine/pyalice",
        "//packages/ml:pyml",
    ],
)

isaac_app(
    name = "inference",
    data = ["@ball_segmentation_model"],
    modules = [
        "//apps/samples/ball_segmentation:ball_segmentation_visualizer",
        "//packages/ml:ml",
        "//packages/ml:tensorflow",
        "//packages/perception",
        "//packages/viewers",
        "zed",
    ],
)

load("//engine/build:pybind.bzl", "pybind_library")
