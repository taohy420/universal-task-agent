import asyncio
import sys

from mcp.client.session import ClientSession
from mcp.client.stdio import StdioServerParameters, stdio_client

MCP_TOOL_SCHEMAS = [
    {
        "type": "function",
        "function": {
            "name": "echo_text",
            "description": "Echo the input text through the MCP simple server.",
            "parameters": {
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "The text to echo.",
                    }
                },
                "required": ["text"],
            },
        },
    }
]

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
                "echo_text",
                {"text": "hello mcp"},
            )
            print("Tool Result:", result.content)


if __name__ == "__main__":
    result = call_mcp_tool_sync("echo_text", {"text": "hello sync mcp"})
    print(result)