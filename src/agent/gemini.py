import json

from google import genai
from google.genai import types

from src.agent import PROMPTS
from src.helpers import ist_now
from src.settings import AI_AGENT_API_KEY, AI_AGENT_MODEL, ALLOW_AGENT_CALL
from src.utils import logger


class GeminiInsightAgenticCall:
    name = "gemini_insight"
    template = PROMPTS

    def __init__(self):
        self.api_key = AI_AGENT_API_KEY
        self.model = AI_AGENT_MODEL
        if not self.api_key or not self.model:
            raise ValueError(f"Missing required values for {self.name}: 'api_key' or 'model'")

    def send(self, prompt: str):
        """
        - Send prompt to Gemini AI and return response
        - Returns: Response text or None if failed/disabled
        """
        if not ALLOW_AGENT_CALL:
            logger.info("AI agent call disabled.")
            return None

        try:
            client = genai.Client(api_key=self.api_key)
            response = client.models.generate_content(
                model=self.model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    thinking_config=types.ThinkingConfig(thinking_budget=0)
                ),
            )
            logger.info(f"{self.name} - Daily insight generated successfully.")
            return response.text
        except Exception as e:
            logger.error(f"{self.name} - Failed to get response from Gemini - {type(e).__name__}: {str(e)}")


    def fetch_prompt(self, insight: str) -> str:
        """Get prompt template for insight type"""
        return self.template.get(insight, "")

    def daily_insight(self, data: dict):
        """Generate daily market insight"""
        try:
            feed = data["items"][0] if len(data.get("items")) > 0 else None
            if not feed:
                raise ValueError(f"no feed fetched for {ist_now()}")

            template = self.fetch_prompt(insight="daily")
            if not template:
                raise ValueError(f"{self.name} - Template not found.")

            context = template.format(json.dumps(feed, default=str))
            return self.send(prompt=context)
        except Exception as e:
            logger.error(f"{self.name} - Failed to generate daily insight - {type(e).__name__}: {str(e)}")

    def weekly_insight(self, data: dict) -> str:
        """Generate weekly market insight"""
        try:
            if not data:
                raise ValueError("data can't be empty")

            template = self.fetch_prompt(insight="weekly")
            if not template:
                raise ValueError(f"{self.name} - Template not found.")

            context = template.format(json.dumps(data))
            return self.send(prompt=context)
        except Exception as e:
            logger.error(f"{self.name} - Failed to generate weekly insight - {type(e).__name__}: {str(e)}")

    def monthly_insight(self, data: list) -> str:
        raise NotImplementedError

    def yearly_insight(self, data: list) -> str:
        raise NotImplementedError
