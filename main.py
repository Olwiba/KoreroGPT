import os
import openai
import pyaudio
import pygame
import wave
from google.cloud import speech_v1p1beta1 as speech
from google.cloud import texttospeech

# Read API key from file.
def read_api_key(file_path):
    with open(file_path, 'r') as file:
        api_key = file.read().strip()
    return api_key

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:/Workspace/KoreroGPT/keys/korerogpt-9f35780d3889.json"
openai.api_key = read_api_key("C:/Workspace/KoreroGPT/keys/openAiKey.txt")

def remove_file(file_path):
    if os.path.isfile(file_path):
        os.remove(file_path)


def play_mp3(file_path):
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

def transcribe_audio_file(file_path):
    client = speech.SpeechClient()
    with open(file_path, "rb") as audio_file:
        content = audio_file.read()

    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="en-US",
    )

    response = client.recognize(config=config, audio=audio)
    return response.results[0].alternatives[0].transcript

def text_to_speech(text, output_file):
    client = texttospeech.TextToSpeechClient()
    input_text = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        ssml_gender=texttospeech.SsmlVoiceGender.FEMALE,
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=input_text, voice=voice, audio_config=audio_config
    )

    with open(output_file, "wb") as out:
        out.write(response.audio_content)

def get_chatgpt_response(prompt):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=50,
        n=1,
        stop=None,
        temperature=0.7,
    )

    return response.choices[0].text.strip()

def record_audio(file_path, seconds=3):
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("Recording...")

    frames = []

    for _ in range(0, int(RATE / CHUNK * seconds)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("Finished recording.")

    stream.stop_stream()
    stream.close()
    p.terminate()

    with wave.open(file_path, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))


# Capture the user's speech input.
# Convert the speech input into text using the STT library.
# Send the text input to ChatGPT and get a response.
# Convert the ChatGPT response into speech using the TTS library.
# Animate the avatar while playing the generated speech.
# Repeat steps 1-5 for an interactive conversation.

def interactive_conversation():
    print("Welcome to KoreroGPT!")
    print("---------------------")
    print("Press Ctrl+C to exit.")
    while True:
        print("Press Enter to Korero...")
        input("")
        
        # 1. Capture the user's speech input
        input_file = "./input.wav"
        record_audio(input_file)

        # 2. Convert the speech input into text using the STT library
        user_text = transcribe_audio_file(input_file)
        print("User: ", user_text)

        # Cleanup input audio file
        # remove_file(input_file)

        # 3. Send the text input to ChatGPT and get a response
        prompt = "User: " + user_text + "\nAssistant:"
        chatgpt_response = get_chatgpt_response(prompt)
        print("KoreroGPT: ", chatgpt_response)

        # 4. Convert the ChatGPT response into speech using the TTS library
        output_file = "./output.mp3"
        text_to_speech(chatgpt_response, output_file)

        # Play the response using a media player, e.g., VLC or mpg123
        play_mp3(output_file)

        # Cleanup output audio file
        # remove_file(output_file)

if __name__ == "__main__":
    interactive_conversation()
