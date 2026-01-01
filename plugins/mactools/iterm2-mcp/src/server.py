"""MCP server for iTerm2 bidirectional control."""

import asyncio
import logging
import sys
from typing import Any

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool

from .iterm_controller import get_controller
from .tools.iterm_tools import TOOLS

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    stream=sys.stderr,  # MCP uses stdout for protocol, stderr for logs
)
logger = logging.getLogger(__name__)


# Create MCP server
app = Server("iterm2-mcp-server")


@app.list_tools()
async def list_tools() -> list[Tool]:
    """List all available MCP tools."""
    return [
        Tool(
            name=tool["name"],
            description=tool["description"],
            inputSchema=tool["inputSchema"],
        )
        for tool in TOOLS
    ]


@app.call_tool()
async def call_tool(name: str, arguments: Any) -> list[Any]:
    """Handle tool calls from MCP clients."""
    # Find tool handler
    tool = next((t for t in TOOLS if t["name"] == name), None)
    if not tool:
        logger.error(f"Unknown tool: {name}")
        return [{"type": "text", "text": f"Error: Unknown tool '{name}'"}]

    try:
        # Call tool handler
        result = await tool["handler"](arguments or {})

        # Format result as MCP response
        if result.get("success"):
            # Success response
            response_text = []

            # Add main message if present
            if "message" in result:
                response_text.append(result["message"])

            # Add session info
            if "session_id" in result:
                response_text.append(f"\nSession ID: {result['session_id']}")

            # Add attach command for shared sessions
            if "attach_command" in result:
                response_text.append(f"\nAttach command: {result['attach_command']}")

            # Add output for read operations
            if "output" in result:
                response_text.append(f"\nOutput:\n{result['output']}")
                if result.get("remaining", 0) > 0:
                    response_text.append(
                        f"\n[{result['remaining']} more lines available]"
                    )

            # Add sessions list
            if "sessions" in result:
                response_text.append("\n\nActive Sessions:")
                for session in result["sessions"]:
                    response_text.append(
                        f"\n  • {session['session_id']} - "
                        f"{session.get('command', 'bash')} "
                        f"({session['controlled_by']}) - "
                        f"{session['runtime_seconds']:.1f}s"
                    )
                    if session.get("tmux_session"):
                        response_text.append(f"    tmux: {session['tmux_session']}")

            # Add warnings
            if "warning" in result:
                response_text.append(f"\n⚠️  {result['warning']}")

            return [{"type": "text", "text": "\n".join(response_text)}]

        else:
            # Error response
            error_msg = result.get("error", "Unknown error")
            logger.error(f"Tool {name} failed: {error_msg}")
            return [{"type": "text", "text": f"Error: {error_msg}"}]

    except Exception as e:
        logger.exception(f"Error executing tool {name}")
        return [{"type": "text", "text": f"Error: {str(e)}"}]


async def main() -> None:
    """Run the MCP server."""
    logger.info("Starting iTerm2 MCP server...")

    # Connect to iTerm2
    controller = await get_controller()
    if not controller.is_connected:
        logger.error(
            "Failed to connect to iTerm2. "
            "Make sure iTerm2 is running and Python API is enabled "
            "(Preferences > General > Magic > Enable Python API)"
        )
        sys.exit(1)

    logger.info("Connected to iTerm2")
    logger.info("Server ready to accept requests")

    # Run MCP server using stdio transport
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options(),
        )


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Server shutdown by user")
    except Exception as e:
        logger.exception("Server error")
        sys.exit(1)
