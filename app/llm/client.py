import os
from dotenv import load_dotenv
from google import genai

load_dotenv()


class LLMClient:
    """
    Gemini-based LLM client using the new SDK.
    """

    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment")

        # Create client (NEW SDK way)
        self.client = genai.Client(api_key=api_key)

        # Use fast, low-latency model
        self.model = "gemini-2.5-flash"

    def generate(self, prompt: str) -> str:
        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
            config={
                "temperature": 0.4,
                "max_output_tokens": 1024,
            },
        )

        return response.text.strip()
