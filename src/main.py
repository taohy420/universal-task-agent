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
    user_input = "请调用 echo_text 工具，把 hello from agent 发送过去。"

    result = run_agent(llm, user_input)
    print(result)


if __name__ == "__main__":
    main()