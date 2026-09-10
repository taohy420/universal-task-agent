WEATHER_SCHEMA = {
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "Get the current weather for a given city.",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": "The city name, for example: Shanghai",
                }
            },
            "required": ["city"],
        },
    },
}


def get_weather(city: str) -> str:
    fake_weather = {
        "Shanghai": "rainy",
        "Beijing": "sunny",
        "Shenzhen": "cloudy",
    }

    return fake_weather.get(city, "unknown")