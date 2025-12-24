


from faster_whisper import WhisperModel
from app.config import WHISPER_MODEL_SIZE, WHISPER_COMPUTE_TYPE


class SpeechToText:
    """
    Handles speech-to-text transcription using Whisper.
    """

    def __init__(self):
        self.model = WhisperModel(
            WHISPER_MODEL_SIZE,
            device="cpu",
            compute_type=WHISPER_COMPUTE_TYPE
        )

    def transcribe(self, audio_path: str) -> str:
        """
        Transcribes an audio file into text.
        """
        segments, _ = self.model.transcribe(audio_path, task="transcribe", beam_size=5)
        transcript = " ".join(segment.text for segment in segments)
        return transcript.strip()
