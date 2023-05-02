import os
import openai
import pyaudio

from pydub import AudioSegment
from pydub.playback import play
from google.cloud import texttospeech
import speech_recognition as sr

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

def text_to_speech(text, output_file):
    client = texttospeech.TextToSpeechClient()
    input_text = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-NZ",
        ssml_gender=texttospeech.SsmlVoiceGender.FEMALE,
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3,
        speaking_rate=1.5,
    )

    response = client.synthesize_speech(
        input=input_text, voice=voice, audio_config=audio_config
    )

    with open(output_file, "wb") as out:
        out.write(response.audio_content)

def get_chatgpt_response(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=50,
        n=1,
        stop=None,
        temperature=0.7,
    )

    return response.choices[0].text.strip()


# Capture the user's speech input.
# Convert the speech input into text using the STT library.
# Send the text input to ChatGPT and get a response.
# Convert the ChatGPT response into speech using the TTS library.
# Animate the avatar while playing the generated speech.
# Repeat steps 1-5 for an interactive conversation.

def interactive_conversation():
    print("⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀")
    print("⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀")
    print("⠀⠀⠀⠀⠀⠀⠀⠀⣀⣀⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣀⣀⠀⠀⠀⠀⠀⠀⠀⠀")
    print("⠀⠀⠀⠀⢀⣴⣾⣿⠿⠟⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠻⠿⣿⣷⣦⡀⠀⠀⠀⠀")
    print("⠀⠀⢀⣾⣿⠟⠉⠀⠀⠀⣠⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣤⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣤⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣄⠀⠀⠀⠈⠻⣿⣷⡀⠀⠀")
    print("⠀⣰⣿⡟⠁⠀⠀⠀⢀⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣾⣿⣿⣿⣿⣿⣿⣷⣄⠀⠀⠀⠀⣠⣾⣿⣿⣝⣯⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⡀⠀⠀⠀⠈⢻⣿⣆⠀")
    print("⢰⣿⡏⠀⠀⠀⠀⠀⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡆⠀⠀⢸⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⠀⠀⠀⠀⠀⢹⣿⡆")
    print("⣾⣿⠀⠀⠀⠀⠀⢰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡆⠀⠀⠀⠀⠀⣿⣷")
    print("⣿⣿⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⡏⠉⠉⠉⠉⣿⣿⣿⣿⣿⣿⣿⠀⠀⣿⣿⣿⣿⣿⣿⣿⠉⠉⠉⠉⢹⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⣿⣿")
    print("⢻⣿⡀⠀⠀⠀⠀⠸⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⠀⠀⢿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⠇⠀⠀⠀⠀⢀⣿⡿")
    print("⠘⣿⣧⠀⠀⠀⠀⠀⢻⣿⣿⣿⣿⣿⣿⣿⣿⣧⣤⣤⣤⣤⣿⣿⣿⣿⣿⣿⠃⠀⠀⠘⣿⣿⣿⣿⣿⣿⣤⣤⣤⣤⣼⣿⣿⣿⣿⣿⣿⣿⣿⡟⠀⠀⠀⠀⠀⣼⣿⠃")
    print("⠀⠘⢿⣷⡀⠀⠀⠀⠀⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠃⠀⠀⠀⠀⠘⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠀⠀⠀⠀⢀⣾⡿⠃⠀")
    print("⠀⠀⠈⠻⣿⣶⣄⡀⠀⠀⠈⠻⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠋⠀⠀⠀⠀⠀⠀⠀⠀⠙⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠟⠁⠀⠀⢀⣠⣶⣿⠟⠁⠀⠀")
    print("⠀⠀⠀⠀⠀⠙⠻⢿⣿⣶⣶⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣶⣶⣿⡿⠟⠋⠁⠀⠀⠀⠀")
    print("⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀")
    print("⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⣶⣶⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣴⣶⣶⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀")
    print("⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀")
    print("                 ╔═════════════════════════╗")
    print("                 ║  Welcome to KoreroGPT!  ║")
    print("                 ╠═════════════════════════╣")
    print("                 ║ * Press Ctrl+C to exit. ║")
    print("                 ║                         ║")
    print("                 ║      Made with <3       ║")
    print("                 ╚═════════════════════════╝")
    print("")

    # Create a recognizer instance
    r = sr.Recognizer()
    
    while True:
        print("Speak to Korero...")

        # Set the microphone as the audio source
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source) # Adjust for ambient noise levels
            audio = r.listen(source) # Listen for audio input

        try:
            print("Processing audio...")
            # Transcribe the audio to text
            user_text = r.recognize_google(audio)
            print("User: ", user_text)

            # Send the text input to ChatGPT and get a response
            prompt = "User: " + user_text + "\nKoreroGPT:"
            chatgpt_response = get_chatgpt_response(prompt)
            print("KoreroGPT: ", chatgpt_response)

            # Convert the ChatGPT response into speech using the TTS library
            output_file = "./output.mp3"
            text_to_speech(chatgpt_response, output_file)

            # Play the response
            audio = AudioSegment.from_file(output_file)
            play(audio)

            # Cleanup output audio file
            remove_file(output_file)

        except sr.UnknownValueError:
            # TODO - this should say something..
            print("Could not understand audio")
        except sr.RequestError as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    interactive_conversation()
