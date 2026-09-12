import asyncio
import sys

from mcp.client.session import ClientSession
from mcp.client.stdio import StdioServerParameters, stdio_client

MCP_TOOL_SCHEMAS = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get the real current weather for a given city through the MCP server.",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "The city name, for example: Shanghai or Beijing.",
                    }
                },
                "required": ["city"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_hot_news",
            "description": "Get the top 3 current hot news headlines through the MCP server.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
            },
        },
    }
]

MCP_TOOL_NAMES = {
    item["function"]["name"]
    for item in MCP_TOOL_SCHEMAS
}

async def call_mcp_tool(tool_name: str, arguments: dict):
    server_params = StdioServerParameters(
        command=sys.executable,
        args=["src/mcp_servers/simple_server.py"],
    )

    async with stdio_client(server_params) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()
            result = await session.call_tool(tool_name, arguments)
            return result.content

def call_mcp_tool_sync(tool_name: str, arguments: dict) -> str:
    result = asyncio.run(call_mcp_tool(tool_name, arguments))

    if result and hasattr(result[0], "text"):
        return result[0].text

    return str(result)

async def main():
    server_params = StdioServerParameters(
        command=sys.executable,
        args=["src/mcp_servers/simple_server.py"],
    )

    async with stdio_client(server_params) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()

            tools = await session.list_tools()
            print("MCP Tools:")
            for tool in tools.tools:
                print("-", tool.name, "|", tool.description)

            result = await session.call_tool(
                "get_hot_news",
                {},
            )
            print("Tool Result:", result.content)


if __name__ == "__main__":
    result = call_mcp_tool_sync("get_hot_news", {})
    print(result)
