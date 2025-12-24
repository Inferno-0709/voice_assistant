import collections
import time
import sounddevice as sd
import numpy as np
import webrtcvad
from scipy.io.wavfile import write

from app.config import SAMPLE_RATE, CHANNELS, TEMP_AUDIO_FILE

# --- Tunable parameters ---
FRAME_DURATION_MS = 30
FRAME_SIZE = int(SAMPLE_RATE * FRAME_DURATION_MS / 1000)

PRE_SPEECH_FRAMES = 15       
SILENCE_FRAMES_TO_STOP = 20   
ENERGY_THRESHOLD = 300        
MAX_RECORD_SECONDS = 15       

def rms_energy(frame: np.ndarray) -> float:
    return np.sqrt(np.mean(frame.astype(np.float32) ** 2))

def record_audio(output_file: str = TEMP_AUDIO_FILE) -> str:
    print("🎙️ Speak now...")

    vad = webrtcvad.Vad(3)  
    pre_buffer = collections.deque(maxlen=PRE_SPEECH_FRAMES)
    recorded = []

    speech_started = False
    silence_counter = 0
    start_time = time.time()

    with sd.InputStream(
        samplerate=SAMPLE_RATE,
        channels=CHANNELS,
        blocksize=FRAME_SIZE,
        dtype="int16",
    ) as stream:

        while True:
            frame, _ = stream.read(FRAME_SIZE)
            pcm_bytes = frame.tobytes()

            energy = rms_energy(frame)
            vad_speech = vad.is_speech(pcm_bytes, SAMPLE_RATE)
            is_speech = vad_speech and energy > ENERGY_THRESHOLD

            
            if not speech_started:
                pre_buffer.append(frame)

                if is_speech:
                    print("🟢 Speech detected")
                    speech_started = True
                    recorded.extend(pre_buffer)
                    pre_buffer.clear()
                    silence_counter = 0

            
            else:
                recorded.append(frame)

                if is_speech:
                    silence_counter = 0
                else:
                    silence_counter += 1

                    if silence_counter >= SILENCE_FRAMES_TO_STOP:
                        print("🛑 Silence detected")
                        break

            
            if time.time() - start_time > MAX_RECORD_SECONDS:
                print("⏱️ Max duration reached")
                break

    if not recorded:
        raise RuntimeError("No speech captured")

    audio = np.concatenate(recorded, axis=0)
    write(output_file, SAMPLE_RATE, audio)

    print(f"💾 Saved audio to {output_file}")
    return output_file
