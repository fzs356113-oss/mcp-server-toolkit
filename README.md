<div align="center">

# 🔌 MCP Server Toolkit

**The fastest way to connect AI agents to the real world.**

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-00D9A0?style=for-the-badge)](LICENSE)
[![MCP Compatible](https://img.shields.io/badge/MCP-Compatible-FF6B35?style=for-the-badge)](https://modelcontextprotocol.io)
[![Stars](https://img.shields.io/github/stars/fzs356113-oss/mcp-server-toolkit?style=for-the-badge&color=FFD700)](https://github.com/fzs356113-oss/mcp-server-toolkit)
[![Forks](https://img.shields.io/github/forks/fzs356113-oss/mcp-server-toolkit?style=for-the-badge)](https://github.com/fzs356113-oss/mcp-server-toolkit/fork)

*A production-ready [Model Context Protocol](https://modelcontextprotocol.io) server toolkit that gives your AI agents superpowers.*

[Quick Start](#-quick-start) · [Features](#-features) · [Architecture](#-architecture) · [Documentation](#-documentation)

</div>

---

## 🎯 Why MCP Server Toolkit?

> Every AI agent needs tools. MCP Server Toolkit gives them **file system access**, **web fetching**, **database queries**, and **shell commands** — all through a single, standardized protocol.

```mermaid
graph LR
    A[🤖 AI Agent] -->|MCP Protocol| B[🔌 MCP Server Toolkit]
    B --> C[📁 File System]
    B --> D[🌐 Web Fetch]
    B --> E[🗄️ Database]
    B --> F[💻 Shell]
```

## ✨ Features

| Tool | Description | Status |
|------|-------------|--------|
| 📁 **File System** | Read, write, search, and manage files | ✅ Production Ready |
| 🌐 **Web Fetch** | Fetch web pages, APIs, and download files | ✅ Production Ready |
| 🗄️ **Database** | Query PostgreSQL, MySQL, SQLite, MongoDB | ✅ Production Ready |
| 💻 **Shell** | Execute commands with sandboxing | ✅ Production Ready |
| 🔐 **Auth** | OAuth2 / API Key / JWT authentication | 🚧 Coming Soon |
| 📊 **Metrics** | Prometheus-compatible metrics endpoint | 🚧 Coming Soon |

## 🚀 Quick Start

### Installation

```bash
pip install mcp-server-toolkit
```

### Run in 30 seconds

```python
from mcp_server import MCPServer, tools

# Create server with default tools
server = MCPServer(
    name="my-agent-tools",
    tools=[tools.FileSystem(), tools.WebFetch(), tools.Database(), tools.Shell()]
)

# Start serving
server.run(port=8080)
```

### Configuration (YAML)

```yaml
# config.yaml
server:
  name: my-mcp-server
  port: 8080
  auth: none

tools:
  filesystem:
    root: /workspace
    allowed_extensions: [.py, .js, .ts, .md]
  web_fetch:
    timeout: 30
    user_agent: "MCP-Toolkit/1.0"
  database:
    url: postgresql://user:pass@localhost:5432/mydb
  shell:
    allowed_commands: [ls, cat, grep, python]
    sandbox: true
```

```bash
mcp-server --config config.yaml
```

## 🏗️ Architecture

```
mcp-server-toolkit/
├── mcp_server/
│   ├── __init__.py          # Public API
│   ├── server.py            # Core MCP server
│   ├── protocol.py          # MCP protocol handler
│   └── tools/
│       ├── filesystem.py    # File operations
│       ├── web_fetch.py     # HTTP client
│       ├── database.py      # DB connectors
│       └── shell.py         # Command executor
├── config.yaml.example      # Example config
├── pyproject.toml
└── README.md
```

## 📖 Documentation

<details>
<summary><b>📁 File System Tool</b></summary>

```python
from mcp_server.tools import FileSystem

fs = FileSystem(root="/workspace")

# Read file
content = await fs.read("src/main.py")

# Write file
await fs.write("output.txt", "Hello, World!")

# Search files
results = await fs.search("**/*.py", pattern="import asyncio")

# List directory
files = await fs.listdir("src/", recursive=True)
```
</details>

<details>
<summary><b>🌐 Web Fetch Tool</b></summary>

```python
from mcp_server.tools import WebFetch

web = WebFetch(timeout=30)

# Fetch page
page = await web.fetch("https://api.github.com/user")

# Download file
await web.download("https://example.com/data.csv", "local.csv")

# Parse HTML
text = await web.extract_text("https://news.ycombinator.com")
```
</details>

<details>
<summary><b>🗄️ Database Tool</b></summary>

```python
from mcp_server.tools import Database

db = Database(url="postgresql://localhost/mydb")

# Query
rows = await db.query("SELECT * FROM users WHERE active = true")

# Insert
await db.insert("users", {"name": "Alice", "role": "admin"})

# Transaction
async with db.transaction() as tx:
    await tx.execute("UPDATE accounts SET balance = balance - 100 WHERE id = 1")
    await tx.execute("UPDATE accounts SET balance = balance + 100 WHERE id = 2")
```
</details>

## 🤝 Contributing

We love contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

```bash
git clone https://github.com/fzs356113-oss/mcp-server-toolkit.git
cd mcp-server-toolkit
pip install -e ".[dev]"
pytest
```

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

---

<div align="center">

**⭐ Star this repo if you find it useful! ⭐**

Made with ❤️ by [fzs356113-oss](https://github.com/fzs356113-oss)

</div>
