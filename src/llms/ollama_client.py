import os
import requests
from dotenv import load_dotenv

from llms.base import BaseLLM


load_dotenv()


class OllamaClient(BaseLLM):
    def __init__(self):
        self.base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        self.model = os.getenv("OLLAMA_MODEL", "qwen2.5:3b")

    def chat(self, messages: list[dict]) -> str:
        response = requests.post(
            f"{self.base_url}/api/chat",
            json={
                "model": self.model,
                "messages": messages,
                "stream": False,
            },
            timeout=60,
        )

        response.raise_for_status()
        data = response.json()
        return data["message"]["content"]