/*
Copyright (c) 2018, NVIDIA CORPORATION. All rights reserved.

NVIDIA CORPORATION and its licensors retain all intellectual property
and proprietary rights in and to this software, related documentation
and any modifications thereto. Any use, reproduction, disclosure or
distribution of this software and related documentation without an express
license agreement from NVIDIA CORPORATION is strictly prohibited.
*/
#include "AudioDataCaptureToFile.hpp"

#include <memory>
#include <string>
#include <vector>

#include "engine/alice/alice_codelet.hpp"
#include "engine/core/buffers.hpp"
#include "messages/messages.hpp"

namespace isaac {

void AudioDataCaptureToFile::start() {
  std::string file_name = get_path();
  if (file_name.empty()) {
    return;
  }

  fp_ = std::fopen(file_name.c_str(), "wb");
  if (!fp_) {
    return;
  }

  tickOnMessage(rx_audio_capture());
}

void AudioDataCaptureToFile::tick() {
  uint8_t number_of_channels = rx_audio_capture().getProto().getNumChannels();
  const std::vector<isaac::ByteBuffer>& byte_buffer_list = rx_audio_capture().buffers();
  if (number_of_channels != byte_buffer_list.size()) {
    PANIC("Channel count does not match %d != %u",
          number_of_channels, byte_buffer_list.size());
  }

  size_t num_samples_per_channel = byte_buffer_list[0].size() / sizeof(float);
  std::unique_ptr<float[]> buffer =
    std::make_unique<float[]>(num_samples_per_channel * number_of_channels);

  // interleave and write to file
  for (size_t c = 0; c < number_of_channels; c++) {
    const float* src = reinterpret_cast<const float*>(byte_buffer_list[c].begin());
    for (size_t s = 0; s < num_samples_per_channel; s++) {
      size_t offset = (s * number_of_channels) + c;
      buffer.get()[offset] = src[s];
    }
  }

  fwrite(buffer.get(), sizeof(float),
         num_samples_per_channel * number_of_channels, fp_);
}

void AudioDataCaptureToFile::stop() {
  if (fp_) {
    fclose(fp_);
  }
}

}  // namespace isaac

