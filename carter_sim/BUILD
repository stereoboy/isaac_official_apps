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
    name = "carter_sim",
    app_json_file = "carter_sim.app.json",
    data = [
        "//apps/assets/maps",
        "//packages/map:libmap_module.so",
        "carter.config.json",
        "carter.graph.json",
        "navigation.graph.json",
        "navigation.config.json",
    ],
    modules = [
        "navigation",
        "perception",
        "planner",
        "viewers",
        "flatsim",
    ],
)

isaac_app(
    name = "carter_sim_joystick",
    app_json_file = "carter_sim_joystick.app.json",
    data = [
        "//apps/assets/maps",
        "//packages/map:libmap_module.so",
        "carter.config.json",
        "carter.graph.json",
        "joystick.config.json",
        "joystick.graph.json",
        "navigation.config.json",
        "navigation.graph.json",
    ],
    modules = [
        "navigation",
        "perception",
        "planner",
        "viewers",
        "flatsim",
        "sensors:joystick"
    ],
)

isaac_app(
    name = "carter_sim_mapping",
    app_json_file = "carter_sim_mapping.app.json",
    data = [
        "//packages/map:libmap_module.so",
        "carter.lua",
        "carter.config.json",
        "carter.graph.json",
        "joystick.config.json",
        "joystick.graph.json",
    ],
    modules = [
        "perception",
        "planner",
        "viewers",
        "flatsim",
        "navigation",
        "navigation:cartographer",
        "sensors:joystick"
    ],
)
