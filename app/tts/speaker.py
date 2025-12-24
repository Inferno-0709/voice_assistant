import os
import tempfile
from gtts import gTTS
from playsound import playsound

from app.config import TEMP_TTS_FILE


class Speaker:
    """
    Converts text to speech and plays it back.
    """

    def speak(self, text: str):
        if not text.strip():
            return

        tts = gTTS(text=text, lang="en")
        tts.save(TEMP_TTS_FILE)

        playsound(TEMP_TTS_FILE)

        os.remove(TEMP_TTS_FILE)

    def generate_file(self, text: str) -> str:
        """
        Generates audio file and returns the path.
        Does NOT play or delete the file.
        """
        if not text.strip():
            return None

        # Create unique temp file to avoid browser caching issues
        fd, path = tempfile.mkstemp(suffix=".mp3")
        os.close(fd)

        tts = gTTS(text=text, lang="en")
        tts.save(path)
        
        return path
