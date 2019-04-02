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
    name = "audio_capture_test",
    srcs = ["AudioDataCaptureToFile.cpp"],
    hdrs = ["AudioDataCaptureToFile.hpp"],
    tags = ["manual"],
    deps = [
        "//engine/alice",
        "//messages",
    ],
)

isaac_app(
    name = "audio_capture",
    app_json_file = "audio_capture.app.json",
    modules = [
        "//apps/samples/audio_capture:audio_capture_test",
        "audio",
    ],
    tags = ["manual"],
)
