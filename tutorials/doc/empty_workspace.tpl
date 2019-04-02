'''
Copyright (c) 2019, NVIDIA CORPORATION. All rights reserved.

NVIDIA CORPORATION and its licensors retain all intellectual property
and proprietary rights in and to this software, related documentation
and any modifications thereto. Any use, reproduction, disclosure or
distribution of this software and related documentation without an express
license agreement from NVIDIA CORPORATION is strictly prohibited.
'''
workspace(name = "empty_workspace")

local_repository(
    name = "isaac",
    path = "$isaac_path",
)

load("@isaac//engine/build:isaac.bzl", "isaac_git_repository", "isaac_new_http_archive")
load("@isaac//third_party:engine.bzl", "isaac_engine_workspace")
load("@isaac//third_party:packages.bzl", "isaac_packages_workspace")
load("@isaac//third_party:ros.bzl", "isaac_ros_workspace")
load("@isaac//third_party:zed.bzl", "isaac_zed_workspace")

isaac_engine_workspace()

isaac_packages_workspace()

isaac_ros_workspace()

isaac_zed_workspace()

# Configures toolchain
load("@isaac//engine/build/toolchain:toolchain.bzl", "toolchain_configure")

toolchain_configure(name = "toolchain")
