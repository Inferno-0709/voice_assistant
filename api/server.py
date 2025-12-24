from fastapi import FastAPI, UploadFile, File
import shutil
import os
import uuid

from app.stt import HinglishSpeechToText
from app.intent import IntentClassifier
from app.response import KrishnaResponder
from app.tts import Speaker
from app.llm.client import LLMClient


app = FastAPI(title="Krishna Voice Assistant")


stt = HinglishSpeechToText()
llm = LLMClient()
intent_classifier = IntentClassifier(llm)
responder = KrishnaResponder(llm)
speaker = Speaker()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.post("/process-audio")
async def process_audio(file: UploadFile = File(...)):
    
    audio_id = f"{uuid.uuid4()}.wav"
    audio_path = os.path.join(UPLOAD_DIR, audio_id)

    with open(audio_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    # 1. STT
    text = stt.transcribe(audio_path)

    # 2. Intent
    intent = intent_classifier.classify(text)

    # 3. Response
    response = responder.generate(intent)

    
    speaker.speak(response)

    return {
        "transcript": text,
        "intent": intent,
        "response": response,
    }
