"""Tests for MCP Server Toolkit tools."""

import pytest


def test_config_load():
    """Test that default config loads successfully."""
    from mcp_server_toolkit.config import load_config
    config = load_config()
    assert "server" in config
    assert "tools" in config
    assert config["server"]["name"] == "mcp-server-toolkit"


def test_config_tool_config():
    """Test tool config extraction."""
    from mcp_server_toolkit.config import load_config, get_tool_config
    config = load_config()
    fs_config = get_tool_config(config, "file_system")
    assert fs_config.get("enabled") is True
    missing = get_tool_config(config, "nonexistent")
    assert missing == {}


def test_server_creation():
    """Test that the server can be created from config."""
    from mcp_server_toolkit.config import load_config
    from mcp_server_toolkit.server import create_server
    config = load_config()
    server = create_server(config)
    assert server is not None
