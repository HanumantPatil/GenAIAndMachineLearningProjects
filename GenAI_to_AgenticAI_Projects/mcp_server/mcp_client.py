"""Test client for the Leave Management MCP server."""

import argparse
import asyncio
import json
import sys

from mcp import Client

DEFAULT_SERVER_URL = "http://127.0.0.1:8000/mcp"


def create_parser() -> argparse.ArgumentParser:
    """Create the command-line argument parser."""
    parser = argparse.ArgumentParser(
        description="Connect to the Leave Management MCP server and test a tool call."
    )
    parser.add_argument(
        "--url",
        default=DEFAULT_SERVER_URL,
        help=f"MCP server URL (default: {DEFAULT_SERVER_URL})",
    )
    parser.add_argument(
        "--employee-id",
        default="E001",
        help="Employee ID used for the balance test (default: E001)",
    )
    return parser


async def test_server(server_url: str, employee_id: str) -> None:
    """Connect to the server, list tools, and request an employee balance."""
    async with Client(server_url, raise_exceptions=True) as client:
        tools_result = await client.list_tools()
        tool_names = [tool.name for tool in tools_result.tools]
        print(f"Connected to: {server_url}")
        print(f"Available tools: {', '.join(tool_names)}")

        if "get_leave_balance" not in tool_names:
            raise RuntimeError("Server does not expose the get_leave_balance tool.")

        result = await client.call_tool(
            "get_leave_balance",
            {"employee_id": employee_id},
        )
        print("Leave balance response:")
        print(json.dumps(result.structured_content, indent=2))


def main() -> int:
    """Run the MCP client and return a process exit code."""
    args = create_parser().parse_args()
    try:
        asyncio.run(test_server(args.url, args.employee_id))
    except KeyboardInterrupt:
        print("Client interrupted.", file=sys.stderr)
        return 130
    except Exception as error:
        print(f"MCP client failed: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
