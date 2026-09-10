from mcp.server.mcpserver import MCPServer


mcp = MCPServer("simple-server")


@mcp.tool()
def echo_text(text: str) -> str:
    return f"MCP received: {text}"


if __name__ == "__main__":
    mcp.run()