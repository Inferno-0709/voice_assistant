# Krishna Voice Assistant

A calming, voice-activated AI companion inspired by the compassionate persona of Krishna.

## How to Run It

1.  **Prerequisites**:
    -   Python 3.9 or higher.
    -   `ffmpeg` installed and added to system PATH (required for audio processing).
    -   A Google Gemini API key.

2.  **Installation**:
    ```bash
    # Install Python dependencies
    pip install -r requirements.txt
    ```

3.  **Configuration**:
    -   Create a `.env` file in the root directory.
    -   Add your Gemini API key: `GEMINI_API_KEY=your_key_here`

4.  **Running the App**:
    -   Run the Gradio UI:
        ```bash
        python ui/gradio_app.py
        ```
    -   Open the URL provided in the terminal (usually `http://127.0.0.1:7860`).
    -   Click "Record & Send" and speak your query.

## Architecture & Technology Choices

### 1. Speech-to-Text (STT)
-   **Choice**: **Oriserve/Whisper-Hindi2Hinglish-Apex** (HuggingFace Transformers).
-   **Reasoning**:
    -   **Hinglish Support**: Specifically fine-tuned for Hindi-English code-switching behavior.
    -   **Accuracy**: Far superior to vanilla Whisper for this specific dialect.
    -   **Offline**: Runs locally (CPU in this config), ensuring privacy and no external API latency (though trades for compute time).

### 2. Large Language Model (LLM)
-   **Choice**: **Google Gemini 2.5 Flash**.
-   **Reasoning**:
    -   **Speed**: "Flash" models are optimized for low latency, critical for voice interaction.
    -   **Context**: Excellent understanding of nuanced personas (like Krishna) and instructions.
    -   **Cost**: Cost-effective for high-frequency interactions.

### 3. Text-to-Speech (TTS)
-   **Choice**: **gTTS (Google Translate TTS)**.
-   **Reasoning**:
    -   **Simplicity**: Extremely easy to integrate and reliable.
    -   **Availability**: Free and requires no complex authentication setup.
    -   *(Note: This is a placeholder for a more emotive TTS like ElevenLabs or derived local models in a production environment)*.

## Latency Breakdown

The total response time is the sum of these sequential steps. Typical approximate values on a standard broadband connection:

| Component | Time (Approx) | Description |
| :--- | :--- | :--- |
| **VAD / Silence** | ~0.6s | Time waiting to confirm user stopped speaking. |
| **STT (Whisper)** | 2.0s - 4.0s | Transcribing audio. Heavy CPU usage if no GPU. |
| **LLM (Gemini)** | ~0.5s - 1.0s | Generating the text response. |
| **TTS (gTTS)** | 1.0s - 2.0s | Generating audio file from text (network call). |
| **Total** | **~4s - 7s** | **Total "Time to Audio"** |

*Note: STT is the biggest bottleneck on CPU-only machines.*

## Known Limitations & Improvements

1.  **Latency**:
    -   *Current*: The sequential pipeline (STT -> LLM -> TTS) creates a noticeable pause.
    -   *Improvement*: Implement **Audio Streaming**. Stream TTS tokens from the LLM directly to the audio player to start speaking *while* the sentence is still being generated.

2.  **Robotic Voice**:
    -   *Current*: gTTS is flat and lacks the "calm, compassionate" depth required for the Krishna persona.
    -   *Improvement*: Use **ElevenLabs** or a fine-tuned **StyleTTS2** model for a rich, deep, and emotive voice.

3.  **Turn-Taking**:
    -   *Current*: Strict "Walkie-Talkie" style. User speaks -> waits -> Bot speaks.
    -   *Improvement*: Implement **Full Duplex / Barge-in**. Allow the user to "interrupt" the bot, requiring echo cancellation and real-time VAD.

4.  **Hardware Dependency**:
    -   *Current*: Deeply dependent on local CPU for STT.
    -   *Improvement*: Move STT to a cloud API (like Deepgram) for sub-500ms transcription.
