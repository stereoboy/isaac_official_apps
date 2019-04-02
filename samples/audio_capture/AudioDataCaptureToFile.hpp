/*
Copyright (c) 2018, NVIDIA CORPORATION. All rights reserved.

NVIDIA CORPORATION and its licensors retain all intellectual property
and proprietary rights in and to this software, related documentation
and any modifications thereto. Any use, reproduction, disclosure or
distribution of this software and related documentation without an express
license agreement from NVIDIA CORPORATION is strictly prohibited.
*/
#pragma once

#include <cstdio>
#include <string>

#include "engine/alice/alice_codelet.hpp"
#include "messages/messages.hpp"

namespace isaac {

// Capture audio data and write to a file
class AudioDataCaptureToFile : public alice::Codelet {
 public:
  // audio data input
  ISAAC_PROTO_RX(AudioDataProto, audio_capture)
  // audio data will be dumped to this file
  ISAAC_PARAM(std::string, path, "/tmp/audio-out-f32-16k.pcm")

  void start() override;
  void tick() override;
  void stop() override;

 private:
  std::FILE* fp_ = nullptr;
};

}  // namespace isaac

ISAAC_ALICE_REGISTER_CODELET(isaac::AudioDataCaptureToFile);
