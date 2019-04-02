"""
Copyright (c) 2019, NVIDIA CORPORATION. All rights reserved.

NVIDIA CORPORATION and its licensors retain all intellectual property
and proprietary rights in and to this software, related documentation
and any modifications thereto. Any use, reproduction, disclosure or
distribution of this software and related documentation without an express
license agreement from NVIDIA CORPORATION is strictly prohibited.
"""

load("//engine/build:isaac.bzl", "isaac_app", "isaac_pkg")
load("//engine/build:pybind.bzl", "pybind_library")

py_binary(
    name = "yolo_training",
    srcs = ["keras-yolo3/yolo_training.py"],
    deps = [
        "//engine/pyalice",
        "//packages/ml:pyml",
    ],
    data = [
        "keras-yolo3/configs/isaac_object_detection.json",
        "keras-yolo3/model_data",
        "yolo_training_apps.config.json",
        "yolo_training_apps.json",
        "@yolo_pretrained_models",
        "//packages/ml:libml_module.so",
        "//packages/perception:libperception_module.so",
        "//packages/sight:libsight_module.so",
        "//packages/viewers:libviewers_module.so",
    ],
)

isaac_app(
    name = "yolo_tensorrt_inference",
    app_json_file = "yolo_tensorrt.app.json",
    data = [
        "@yolo_tensorrt_test_data",
    ],
    modules = [
        "dummies",
        "ml",
        "viewers",
        "yolo",
        "zed",
    ],
)

isaac_pkg(
    name = "yolo_tensorrt-pkg",
    srcs = [
        ":yolo_tensorrt_inference",
    ],
)

py_library(
    name = "keras_to_darknet",
    srcs = ["keras_to_darknet.py"],
)
