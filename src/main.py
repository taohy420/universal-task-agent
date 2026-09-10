from config import LLM_PROVIDER
from llms.deepseek_client import DeepSeekClient
from llms.ollama_client import OllamaClient


def create_llm():
    if LLM_PROVIDER == "deepseek":
        return DeepSeekClient()

    if LLM_PROVIDER == "ollama":
        return OllamaClient()

    raise ValueError(f"Unsupported LLM_PROVIDER: {LLM_PROVIDER}")


def main():
    llm = create_llm()

    messages = [
        {"role": "system", "content": "你是一个简洁的 AI Agent 项目助手。"},
        {"role": "user", "content": "用一句话解释什么是 Agent。"},
    ]

    answer = llm.chat(messages)
    print(answer)


if __name__ == "__main__":
    main()