![](robot-banner.png)

# 🤖 KoreroGPT

This system provides our AI models with a voice interface to make human interaction more accessable.

![image](https://user-images.githubusercontent.com/14970658/236709035-7dd4a5af-43f0-439d-97f2-aeeacc2f4937.png)

### Features 🎉
- Integrated with chatGPT
- Integrated with voice recognition model
- Free chat mode (main.py)
- Awakening word detection mode (mainAwaken.py)
- Keypress mode (mainManual.py)

### Requirements ✅
You will need the following service keys to run this project:
- Python 3.6 or higher
- Google cloud API key - https://console.cloud.google.com/apis/credentials
- Open API key - https://platform.openai.com/

### How to use 📚
Follow these steps to get up and ruinning in no time.

1. Pull down the repository
2. Run `pip install -r requirements.txt`
3. Create and move into `./keys` directory
4. Add your keys
   - Create a `openAiKey.txt` with your openAI key inside
   - Copy your Google cloud API key file (.json) into the directory
5. Modify GOOGLE_APPLICATION_CREDENTIALS in `VoiceQuerier.py` to match your key file name
6. Move to the project root
7. Run the selected mode to start 🚀

```CSS
If you like this project, please give it a star ⭐
```
