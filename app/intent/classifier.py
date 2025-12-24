from app.config import INTENT_LABELS


class IntentClassifier:
    """
    Uses an LLM to classify user intent into predefined categories.
    """

    def __init__(self, llm_client):
        self.llm = llm_client

    def classify(self, text: str) -> str:
        prompt = f"""
You are an intent classification system.

Choose exactly ONE category from the list below:
{", ".join(INTENT_LABELS)}

User message:
"{text}"

Respond with only the category name.
"""

        response = self.llm.generate(prompt).strip()

        # Safety fallback
        if response not in INTENT_LABELS:
            return "Daily Struggles"

        return response
