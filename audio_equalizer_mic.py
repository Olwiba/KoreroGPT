import pyaudio
import numpy as np
import time

# Parameters
CHUNK = 1024
RATE = 44100

# Initialize PyAudio
audio = pyaudio.PyAudio()

# Get the default input device information
input_device_info = audio.get_device_info_by_index(audio.get_default_input_device_info()["index"])
CHANNELS = int(input_device_info["maxInputChannels"])

print(f"Input device: {input_device_info['name']}")
print(f"Max input channels: {CHANNELS}")

# Callback function to process audio data
def audio_input_callback(in_data, frame_count, time_info, status):
    audio_data = np.frombuffer(in_data, dtype=np.int16)
    audio_data = audio_data.reshape(-1, CHANNELS)

    channel_peaks = [np.abs(audio_data[:, i]).max() for i in range(CHANNELS)]

    print(f"Channel peaks: {channel_peaks}", end='\r', flush=True)

    return (in_data, pyaudio.paContinue)

# Open audio stream
stream = audio.open(format=pyaudio.paInt16, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK, stream_callback=audio_input_callback)

# Start audio stream
stream.start_stream()

# Run indefinitely
try:
    while stream.is_active():
        time.sleep(0.1)
except KeyboardInterrupt:
    print("\nStopping audio stream...")

# Stop audio stream
stream.stop_stream()
stream.close()

# Terminate PyAudio
audio.terminate()
