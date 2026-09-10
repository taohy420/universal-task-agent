from llms.deepseek_client import DeepSeekClient
from tools.calculator import CALCULATOR_SCHEMA, calculator
import json


def main():
    llm = DeepSeekClient()

    messages = [
        {"role": "system", "content": "你是一个会根据需要调用工具的 AI Agent。"},
        {"role": "user", "content": "请计算 23 * 17。"},
    ]

    message = llm.chat(messages, tools=[CALCULATOR_SCHEMA])
    print(message)
    tool_call = message["tool_calls"][0]
    tool_name = tool_call["function"]["name"]
    arguments_text = tool_call["function"]["arguments"]

    print("Tool Name:", tool_name)
    print("Arguments Text:", arguments_text)
    arguments = json.loads(arguments_text)
    expression = arguments["expression"]

    print("Expression:", expression)
    observation = calculator(expression)
    print("Observation:", observation)
    messages.append(message)
    messages.append({
    "role": "tool",
    "tool_call_id": tool_call["id"],
    "content": observation,
    })
    print(messages)
    final_message = llm.chat(messages)
    print("Final Answer:", final_message["content"])


if __name__ == "__main__":
    main()