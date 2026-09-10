from config import MAX_STEPS
from tools.registry import get_tool_schemas, execute_tool
import json


def run_agent(llm, user_input: str) -> str:
    messages = [
        {"role": "system", "content": "你是一个会根据需要调用工具的 AI Agent。"},
        {"role": "user", "content": user_input},
    ]

    for step in range(MAX_STEPS):
        message = llm.chat(messages, tools=get_tool_schemas())

        if "tool_calls" not in message:
            return message["content"]

        messages.append(message)

        tool_call = message["tool_calls"][0]
        tool_name = tool_call["function"]["name"]
        arguments_text = tool_call["function"]["arguments"]
        arguments = json.loads(arguments_text)

        observation = execute_tool(tool_name, arguments)

        messages.append({
            "role": "tool",
            "tool_call_id": tool_call["id"],
            "content": observation,
    })

    if "tool_calls" not in message:
        return message["content"]

    return "Agent stopped because it reached MAX_STEPS."