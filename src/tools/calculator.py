CALCULATOR_SCHEMA = {
    "type": "function",
    "function": {
        "name": "calculator",
        "description": "Calculate a mathematical expression and return the result.",
        "parameters": {
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": "The mathematical expression to calculate, for example: 23 * 17",
                }
            },
            "required": ["expression"],
        },
    },
}

def calculator(expression: str) -> str:
    # TODO: eval 不安全，以后应该用安全的表达式解析器来替代。
    result = eval(expression)
    return str(result)