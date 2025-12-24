import torch
from transformers import AutoProcessor, AutoModelForSpeechSeq2Seq, pipeline

MODEL_ID = "Oriserve/Whisper-Hindi2Hinglish-Apex"


class HinglishSpeechToText:
    """
    Hinglish-optimized Whisper ASR using Oriserve fine-tuned model.
    """

    def __init__(self):
        device = "cpu"

        self.processor = AutoProcessor.from_pretrained(MODEL_ID)
        self.model = AutoModelForSpeechSeq2Seq.from_pretrained(
            MODEL_ID,
            torch_dtype=torch.float32,
            low_cpu_mem_usage=True,
        ).to(device)

        self.asr = pipeline(
            "automatic-speech-recognition",
            model=self.model,
            tokenizer=self.processor.tokenizer,
            feature_extractor=self.processor.feature_extractor,
            device=-1,  # CPU
            generate_kwargs={"task": "transcribe"},
        )

    def transcribe(self, audio_path: str) -> str:
        result = self.asr(audio_path)
        return result["text"].strip()
