from tools.calculator import CALCULATOR_SCHEMA, calculator
from tools.weather import WEATHER_SCHEMA, get_weather
from tools.save_note import SAVE_NOTE_SCHEMA, save_note
from mcp_client.client import MCP_TOOL_SCHEMAS, call_mcp_tool_sync


LOCAL_TOOL_FUNCTIONS = {
    "calculator": calculator,
    "get_weather": get_weather,
    "save_note": save_note,
}


TOOL_SCHEMAS = [
    CALCULATOR_SCHEMA,
    WEATHER_SCHEMA,
    SAVE_NOTE_SCHEMA,
    *MCP_TOOL_SCHEMAS,
]


def get_tool_schemas() -> list[dict]:
    return TOOL_SCHEMAS


def execute_tool(tool_name: str, arguments: dict) -> str:
    if tool_name in LOCAL_TOOL_FUNCTIONS:
        tool_function = LOCAL_TOOL_FUNCTIONS[tool_name]

        try:
            return tool_function(**arguments)
        except Exception as error:
            return f"Tool error: {error}"

    if tool_name == "echo_text":
        return call_mcp_tool_sync(tool_name, arguments)

    return f"Tool error: unknown tool '{tool_name}'"