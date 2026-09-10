import os
import requests
from dotenv import load_dotenv

from llms.base import BaseLLM


load_dotenv()


class DeepSeekClient(BaseLLM):
    def __init__(self):
        self.api_key = os.getenv("DEEPSEEK_API_KEY")
        self.model = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")
        self.base_url = "https://api.deepseek.com/chat/completions"

    def chat(self, messages: list[dict]) -> str:
        response = requests.post(
            self.base_url,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": self.model,
                "messages": messages,
                "stream": False,
            },
            timeout=30,
        )

        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"]