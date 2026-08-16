from gtts import gTTS
import tempfile

def speak(text):
    tts = gTTS(text=text, lang="en")

    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as f:
        filename = f.name

    tts.save(filename)
    return filename
