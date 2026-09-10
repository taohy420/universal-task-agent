import json

from config import MAX_STEPS
from tools.registry import get_tool_schemas, execute_tool
from agent.trace import format_trace


def run_agent(llm, user_input: str) -> str:
    messages = [
        {"role": "system", "content": "你是一个会根据需要调用工具的 AI Agent。"},
        {"role": "user", "content": user_input},
    ]

    trace_steps = []

    for step in range(MAX_STEPS):
        message = llm.chat(messages, tools=get_tool_schemas())

        if "tool_calls" not in message:
            final_answer = message["content"]
            return format_trace(trace_steps, final_answer)

        messages.append(message)

        tool_call = message["tool_calls"][0]
        tool_name = tool_call["function"]["name"]
        arguments_text = tool_call["function"]["arguments"]

        try:
            arguments = json.loads(arguments_text)
        except json.JSONDecodeError as error:
            observation = f"Tool error: invalid JSON arguments: {error}"
        else:
            observation = execute_tool(tool_name, arguments)

        trace_steps.append({
            "step": step + 1,
            "tool_name": tool_name,
            "arguments": arguments_text,
            "observation": observation,
        })

        messages.append({
            "role": "tool",
            "tool_call_id": tool_call["id"],
            "content": observation,
        })

    return format_trace(
        trace_steps,
        f"Agent stopped because it reached the maximum step limit: {MAX_STEPS}",
    )