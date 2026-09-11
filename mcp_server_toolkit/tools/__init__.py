"""MCP tools registration."""

from mcp_server_toolkit.tools.file_system import register_file_system_tools
from mcp_server_toolkit.tools.web_fetch import register_web_fetch_tools
from mcp_server_toolkit.tools.database import register_database_tools
from mcp_server_toolkit.tools.shell import register_shell_tools

__all__ = [
    "register_file_system_tools",
    "register_web_fetch_tools",
    "register_database_tools",
    "register_shell_tools",
]
