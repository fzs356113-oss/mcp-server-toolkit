"""MCP Server implementation using the official MCP SDK."""

import argparse
import logging
import sys

from mcp.server.fastmcp import FastMCP

from mcp_server_toolkit.config import load_config, get_tool_config
from mcp_server_toolkit.tools import (
    register_file_system_tools,
    register_web_fetch_tools,
    register_database_tools,
    register_shell_tools,
)

logger = logging.getLogger(__name__)


def create_server(config: dict) -> FastMCP:
    """Create and configure an MCP server from the given config."""
    server_config = config.get("server", {})
    name = server_config.get("name", "mcp-server-toolkit")
    mcp = FastMCP(name)

    file_cfg = get_tool_config(config, "file_system")
    if file_cfg:
        register_file_system_tools(mcp, file_cfg)
        logger.info("Registered file_system tools")

    web_cfg = get_tool_config(config, "web_fetch")
    if web_cfg:
        register_web_fetch_tools(mcp, web_cfg)
        logger.info("Registered web_fetch tools")

    db_cfg = get_tool_config(config, "database")
    if db_cfg:
        register_database_tools(mcp, db_cfg)
        logger.info("Registered database tools")

    shell_cfg = get_tool_config(config, "shell")
    if shell_cfg:
        register_shell_tools(mcp, shell_cfg)
        logger.info("Registered shell tools")

    return mcp


def main():
    """CLI entry point for the MCP server."""
    parser = argparse.ArgumentParser(description="MCP Server Toolkit")
    parser.add_argument("--config", "-c", type=str, default=None, help="Path to YAML config file")
    parser.add_argument("--log-level", type=str, default="INFO", choices=["DEBUG", "INFO", "WARNING", "ERROR"])
    args = parser.parse_args()

    logging.basicConfig(level=getattr(logging, args.log_level), format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    try:
        config = load_config(args.config)
    except FileNotFoundError as e:
        logger.error(str(e))
        sys.exit(1)

    server = create_server(config)
    transport = config.get("server", {}).get("transport", "stdio")
    logger.info(f"Starting MCP server via {transport}")
    server.run(transport=transport)


if __name__ == "__main__":
    main()
