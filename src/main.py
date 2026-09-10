from config import LLM_PROVIDER
from llms.deepseek_client import DeepSeekClient
from llms.ollama_client import OllamaClient
from agent.loop import run_agent
import sys

DEMO_CASES = {
    "1": "请计算 12 * 8 + 5,并把结果保存成笔记。",
    "2": "请查询 Shanghai 的天气，如果下雨，就把今天带伞保存成笔记。",
    "3": "请调用 echo_text 工具发送 hello mcp agent,然后把返回结果保存成笔记。",
}

def create_llm():
    if LLM_PROVIDER == "deepseek":
        return DeepSeekClient()
    elif LLM_PROVIDER == "ollama":
        return OllamaClient()
    else:
        raise ValueError(f"Unsupported LLM provider: {LLM_PROVIDER}")

def main():

    llm = create_llm()
    case_id = sys.argv[1] if len(sys.argv) > 1 else "1"
    if case_id not in DEMO_CASES:
        raise ValueError(f"Unknown demo case: {case_id}")
    user_input = DEMO_CASES[case_id]

    result = run_agent(llm, user_input)
    print(result)


if __name__ == "__main__":
    main()