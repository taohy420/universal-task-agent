def format_trace(trace_steps: list[dict], final_answer: str) -> str:
    lines = []

    for item in trace_steps:
        lines.append(f"Step {item['step']}")
        lines.append(f"Tool Call: {item['tool_name']}")
        lines.append(f"Arguments: {item['arguments']}")
        lines.append(f"Observation: {item['observation']}")
        lines.append("")

    lines.append(f"Final Answer: {final_answer}")

    return "\n".join(lines)