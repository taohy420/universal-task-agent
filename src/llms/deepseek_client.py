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

    def chat(self, messages: list[dict], tools: list[dict] | None = None) -> dict:
        payload = {
                     "model": self.model,
                     "messages": messages,
                    "stream": False,
    }

        if tools:
                payload["tools"] = tools
                payload["tool_choice"] = "auto"

        response = requests.post(
        self.base_url,
        headers={
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        },
        json=payload,
        timeout=30,
    )

        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]