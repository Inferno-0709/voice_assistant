"""
Global configuration for the voice-first intent classifier.
All tunable system parameters live here.
"""

# =========================
# AUDIO SETTINGS
# =========================
SAMPLE_RATE = 16000          # Standard for speech models
CHANNELS = 1                # Mono audio
SILENCE_THRESHOLD = 0.09    # Volume level considered silence
SILENCE_DURATION = 0.7      # Seconds of silence before stopping recording


# =========================
# STT SETTINGS
# =========================
WHISPER_MODEL_SIZE = "large"    # small = balance of speed & accuracy
WHISPER_COMPUTE_TYPE = "float32"   # Faster inference on CPU


# =========================
# INTENT CLASSIFICATION
# =========================
INTENT_LABELS = [
    "Career / Purpose",
    "Relationships",
    "Inner Conflict",
    "Life Transitions",
    "Daily Struggles"
]


# =========================
# RESPONSE GENERATION
# =========================
MAX_RESPONSE_SENTENCES = 2


# =========================
# FILE PATHS
# =========================
TEMP_AUDIO_FILE = "input.wav"
TEMP_TTS_FILE = "response.mp3"
