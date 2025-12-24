"""
Global configuration for the voice-first intent classifier.
All tunable system parameters live here.
"""

# =========================
# AUDIO SETTINGS
# =========================
SAMPLE_RATE = 16000         
CHANNELS = 1                
SILENCE_THRESHOLD = 0.09   
SILENCE_DURATION = 0.7      


# =========================
# STT SETTINGS
# =========================
WHISPER_MODEL_SIZE = "large"    
WHISPER_COMPUTE_TYPE = "float32"   


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
