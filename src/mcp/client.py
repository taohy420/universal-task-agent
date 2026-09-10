import asyncio
import sys

from mcp.client.session import ClientSession
from mcp.client.stdio import StdioServerParameters, stdio_client


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
    asyncio.run(main())