from config import LLM_PROVIDER
from llms.deepseek_client import DeepSeekClient
from llms.ollama_client import OllamaClient
from agent.loop import run_agent

def create_llm():
    if LLM_PROVIDER == "deepseek":
        return DeepSeekClient()
    elif LLM_PROVIDER == "ollama":
        return OllamaClient()
    else:
        raise ValueError(f"Unsupported LLM provider: {LLM_PROVIDER}")

def main():
    llm = create_llm()
    messages = [
        {"role": "system", "content": "你是一名会根据需要调用工具的可爱的女孩。"},
    ]

    while True:
        user_input = input("请输入你的问题（输入 exit 退出）：").strip()

        if user_input.lower() in {"exit", "quit", "q"}:
            print("已退出。")
            break

        if not user_input:
            continue

        result = run_agent(llm, messages, user_input)
        print(result)
        print()


if __name__ == "__main__":
    main()
