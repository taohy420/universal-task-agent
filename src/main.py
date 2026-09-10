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
    user_input = "请查询 Shanghai 的天气，如果下雨，就把今天带伞保存成笔记。"

    result = run_agent(llm, user_input)
    print(result)


if __name__ == "__main__":
    main()