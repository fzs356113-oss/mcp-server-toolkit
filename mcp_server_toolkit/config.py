"""Configuration loader for MCP Server Toolkit."""

import os
import yaml
from pathlib import Path
from typing import Any


DEFAULT_CONFIG_PATH = Path(__file__).parent.parent / "config" / "default.yaml"


def _expand_env_vars(value: Any) -> Any:
    """Recursively expand environment variables in config values."""
    if isinstance(value, str):
        return os.path.expandvars(value)
    if isinstance(value, dict):
        return {k: _expand_env_vars(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_expand_env_vars(v) for v in value]
    return value


def load_config(path: str | Path | None = None) -> dict[str, Any]:
    """Load and validate configuration from a YAML file."""
    config_path = Path(path) if path else DEFAULT_CONFIG_PATH
    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")
    with open(config_path) as f:
        raw = yaml.safe_load(f) or {}
    return _expand_env_vars(raw)


def get_tool_config(config: dict, tool_name: str) -> dict:
    """Extract configuration for a specific tool."""
    tools = config.get("tools", {})
    tool_cfg = tools.get(tool_name, {})
    if not tool_cfg.get("enabled", False):
        return {}
    return tool_cfg
