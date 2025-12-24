from app import intent
from app.config import MAX_RESPONSE_SENTENCES


class KrishnaResponder:
    """
    Generates calm, Krishna-like acknowledgments based on intent.
    """

    def __init__(self, llm_client):
        self.llm = llm_client

    def generate(self, intent: str) -> str:
        prompt = f"""
You are Krishna — calm, compassionate, and reflective.

A person is struggling with the following life theme:
"{intent}"

Speak to them gently as a guide and companion.
Acknowledge their feelings with warmth and depth.
Do NOT give direct advice or instructions.
Use {MAX_RESPONSE_SENTENCES} complete sentences.
Avoid being vague or one-word responses. Ensure your response is complete and not cut off.
"""



        return self.llm.generate(prompt).strip()
