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
    name = "audio_playback_test",
    srcs = ["AudioPlaybackFileIndex.cpp"],
    hdrs = ["AudioPlaybackFileIndex.hpp"],
    tags = ["manual"],
    deps = [
        "//engine/alice",
        "//messages",
    ],
)

isaac_app(
    name = "audio_playback",
    app_json_file = "audio_playback.app.json",
    modules = [
        "//apps/samples/audio_playback:audio_playback_test",
        "audio",
    ],
    data = ["@audio_assets//audio"],
    tags = ["manual"],
)
