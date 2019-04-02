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
    name = "flatsim",
    script = "flatsim.sh",
    modules = [
        "flatsim",
        "map",
        "navigation",
        "planner",
    ],
    data = [
        "demo_1.config.json",
        "demo_1.graph.json",
        "demo_2.config.json",
        "demo_2.graph.json",
        "//apps/assets/maps"
    ]
)
