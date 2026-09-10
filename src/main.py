from llms.deepseek_client import DeepSeekClient
from tools.registry import get_tool_schemas, execute_tool
import json


def main():
    llm = DeepSeekClient()

    messages = [
        {"role": "system", "content": "你是一个会根据需要调用工具的 AI Agent。"},
        {"role": "user", "content": "请计算 100 / 4 + 6。"},
    ]

    message = llm.chat(messages, tools=get_tool_schemas())
    tool_call = message["tool_calls"][0]
    tool_name = tool_call["function"]["name"]
    arguments_text = tool_call["function"]["arguments"]

    print("Tool Name:", tool_name)
    print("Arguments Text:", arguments_text)
    arguments = json.loads(arguments_text)

    observation = execute_tool(tool_name, arguments)
    print("Observation:", observation)
    messages.append(message)
    messages.append({
    "role": "tool",
    "tool_call_id": tool_call["id"],
    "content": observation,
    })
    final_message = llm.chat(messages)
    print("Final Answer:", final_message["content"])


if __name__ == "__main__":
    main()