# MCP Server Toolkit

[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![MCP](https://img.shields.io/badge/MCP-compatible-orange.svg)](https://modelcontextprotocol.io)

A production-ready **Model Context Protocol (MCP) server toolkit** for connecting AI agents to external tools — file system access, web fetching, database queries, and shell commands.

## Features

| Tool Type | Description |
|-----------|-------------|
| **file_system** | Read, write, list, and manage files and directories |
| **web_fetch** | Fetch web pages and APIs with configurable headers and methods |
| **database** | Execute SQL queries via SQLAlchemy (SQLite, PostgreSQL, MySQL, etc.) |
| **shell** | Run shell commands with timeout and output capture |

## Quick Start

```bash
pip install -e .
mcp-server-toolkit
mcp-server-toolkit --config config/production.yaml
```

## Configuration

Edit `config/default.yaml` to enable/disable tools and set parameters:

```yaml
server:
  name: mcp-server-toolkit
  version: "1.0.0"
  transport: stdio

tools:
  file_system:
    enabled: true
    allowed_paths:
      - "${HOME}/workspace"
  web_fetch:
    enabled: true
    timeout: 30
  database:
    enabled: true
    connection_string: "sqlite:///data.db"
  shell:
    enabled: true
    allowed_commands:
      - ls
      - cat
      - python
```

## Programmatic Usage

```python
from mcp_server_toolkit.server import create_server
from mcp_server_toolkit.config import load_config

config = load_config("config/default.yaml")
server = create_server(config)
server.run()
```

## License

MIT — see [LICENSE](LICENSE).
