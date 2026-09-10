from tools.calculator import CALCULATOR_SCHEMA, calculator
from tools.weather import WEATHER_SCHEMA, get_weather
from tools.save_note import SAVE_NOTE_SCHEMA, save_note


TOOL_SCHEMAS = [
    CALCULATOR_SCHEMA,
    WEATHER_SCHEMA,
    SAVE_NOTE_SCHEMA,
]


TOOL_FUNCTIONS = {
    "calculator": calculator,
    "get_weather": get_weather,
    "save_note": save_note,
}


def get_tool_schemas() -> list[dict]:
    return TOOL_SCHEMAS


def execute_tool(tool_name: str, arguments: dict) -> str:
    tool_function = TOOL_FUNCTIONS[tool_name]
    return tool_function(**arguments)