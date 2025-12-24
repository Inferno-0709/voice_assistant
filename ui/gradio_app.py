import gradio as gr
import time
from app.audio.recorder import record_audio
from app.stt import HinglishSpeechToText
from app.intent import IntentClassifier
from app.response import KrishnaResponder
from app.llm.client import LLMClient
from app.tts.speaker import Speaker
import os


try:
    stt = HinglishSpeechToText()
    llm = LLMClient()
    intent_classifier = IntentClassifier(llm)
    responder = KrishnaResponder(llm)
    speaker = Speaker()
except Exception as e:
    print(f"Error initializing components: {e}")

def process_conversation(history):
    """
    Handles a single conversational turn:
    1. Listens for audio (VAD)
    2. Transcribes
    3. Generates response
    4. Speak (returns audio to UI)
    """
    if history is None:
        history = []
        
    # 1. Record (Blocks until silence detected)
    try:
        print("\nListening...")
        audio_path = record_audio()
    except Exception as e:
        print(f"Recording error or timeout: {e}")
        return history, None
        
    # 2. STT
    print("Transcribing...")
    try:
        user_text = stt.transcribe(audio_path)
        print(f"User: {user_text}")
    except Exception as e:
        print(f"STT Error: {e}")
        return history, None
    
    # 3. Intent & Response
    try:
        intent = intent_classifier.classify(user_text)
        bot_text = responder.generate(intent)
        print(f"Bot: {bot_text}")
    except Exception as e:
        print(f"LLM Error: {e}")
        bot_text = "I am having trouble understanding. Please speak again."
    
    # 4. TTS
    audio_file = None
    try:
        audio_file = speaker.generate_file(bot_text)
    except Exception as e:
        print(f"TTS Error: {e}")
    
    # Update history
    history.append({"role": "user", "content": user_text})
    history.append({"role": "assistant", "content": bot_text})
    
   
    if audio_file:
        print(f"Generated audio file: {audio_file}")
        if not os.path.exists(audio_file):
            print("ERROR: Audio file does not exist!")
    else:
        print("No audio file generated.")

    return history, audio_file


with gr.Blocks(title="Krishna Voice Assistant") as demo:
    gr.Markdown("## 🕉️ Krishna – Voice Assistant")
    gr.Markdown("""
    **Instructions:**
    1. Click **Record & Send**.
    2. Speak into your microphone.
    3. The system detects silence, responds, and stops.
    4. Click again to continue.
    """)
    
    chatbot = gr.Chatbot(label="Conversation")
    
    # Hidden audio player with autoplay
    audio_player = gr.Audio(autoplay=True, visible=True, label="Bot Voice")

    with gr.Row():
        start_btn = gr.Button("Record & Send", variant="primary")
        stop_btn = gr.Button("Stop", variant="stop")
    
    # State
    history_state = gr.State([])

    # Events
    loop_event = start_btn.click(
        process_conversation,
        inputs=[history_state],
        outputs=[chatbot, audio_player]
    )
    
    stop_btn.click(
        fn=None,
        inputs=None,
        outputs=None,
        cancels=[loop_event]
    )

if __name__ == "__main__":
    demo.launch()
