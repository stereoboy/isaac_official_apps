'''
Copyright (c) 2019, NVIDIA CORPORATION. All rights reserved.

NVIDIA CORPORATION and its licensors retain all intellectual property
and proprietary rights in and to this software, related documentation
and any modifications thereto. Any use, reproduction, disclosure or
distribution of this software and related documentation without an express
license agreement from NVIDIA CORPORATION is strictly prohibited.
'''
load("//engine/build:isaac.bzl", "isaac_cc_module", "isaac_app", "isaac_component", "isaac_pkg")

isaac_cc_module(
    name = "carter_delivery_codelet",
    srcs = ["CarterDelivery.cpp"],
    hdrs = ["CarterDelivery.hpp"],
    visibility = ["//visibility:public"],
    deps = [
      "//engine/alice",
      "//engine/gems/algorithm:string_utils",
      "//engine/gems/state_machine",
      "//messages",
    ]
)

isaac_app(
    name = "carter_delivery",
    script = "select_json.sh",
    modules = [
      "//apps/carter/carter_delivery:carter_delivery_codelet",
      "communications",
      "map",
      "navigation",
      "perception",
      "perception:april_tags",
      "planner",
      "segway",
      "sensors:joystick",
      "velodyne",
      "viewers",
      "zed"
    ],
    data = [
      "//apps/assets/maps",
      "//apps/carter/robots",
      "//apps/carter/carter_delivery/operators"
    ]
)