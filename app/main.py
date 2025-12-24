from app.audio.recorder import record_audio
from app.stt import SpeechToText
from app.intent import IntentClassifier
from app.response import KrishnaResponder
from app.tts import Speaker
from app.llm.client import LLMClient
from app.utils.timer import Timer


def main():
    timer = Timer()

    stt = SpeechToText()
    llm = LLMClient()
    intent_classifier = IntentClassifier(llm)
    responder = KrishnaResponder(llm)
    speaker = Speaker()

    # 1. Record audio (not counted in latency)
    audio_path = record_audio()

    # 2. STT
    timer.start("Speech to Text")
    text = stt.transcribe(audio_path)
    timer.stop("Speech to Text")
    print("📝 Transcript:", text)

    # 3. Intent classification
    timer.start("Intent Classification")
    intent = intent_classifier.classify(text)
    timer.stop("Intent Classification")
    print("🎯 Intent:", intent)

    # 4. Response generation
    timer.start("Response Generation")
    response = responder.generate(intent)
    timer.stop("Response Generation")
    print("🕉️ Krishna:", response)

    # 5. TTS
    timer.start("Text to Speech")
    speaker.speak(response)
    timer.stop("Text to Speech")

    # Report latency
    timer.report()


if __name__ == "__main__":
    main()
