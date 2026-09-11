"""File system tools for MCP Server Toolkit."""

import os
from pathlib import Path
from mcp.server.fastmcp import FastMCP


def register_file_system_tools(mcp: FastMCP, config: dict) -> None:
    """Register file system tools with the MCP server."""
    allowed_paths = [Path(p).resolve() for p in config.get("allowed_paths", ["."])]
    max_size = config.get("max_file_size_mb", 10) * 1024 * 1024

    def _is_allowed(path: Path) -> bool:
        resolved = path.resolve()
        return any(str(resolved).startswith(str(a)) for a in allowed_paths)

    @mcp.tool()
    def read_file(path: str) -> str:
        """Read the contents of a file."""
        p = Path(path).resolve()
        if not _is_allowed(p):
            return f"Error: Path not allowed: {path}"
        if not p.exists():
            return f"Error: File not found: {path}"
        if p.stat().st_size > max_size:
            return f"Error: File too large (max {config.get('max_file_size_mb', 10)}MB)"
        try:
            return p.read_text(encoding="utf-8")
        except Exception as e:
            return f"Error reading file: {e}"

    @mcp.tool()
    def write_file(path: str, content: str) -> str:
        """Write content to a file. Creates parent directories if needed."""
        p = Path(path).resolve()
        if not _is_allowed(p):
            return f"Error: Path not allowed: {path}"
        try:
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(content, encoding="utf-8")
            return f"Successfully wrote {len(content)} bytes to {path}"
        except Exception as e:
            return f"Error writing file: {e}"

    @mcp.tool()
    def list_directory(path: str = ".") -> str:
        """List files and directories in a path."""
        p = Path(path).resolve()
        if not _is_allowed(p):
            return f"Error: Path not allowed: {path}"
        if not p.is_dir():
            return f"Error: Not a directory: {path}"
        try:
            entries = []
            for entry in sorted(p.iterdir()):
                kind = "d" if entry.is_dir() else "f"
                size = entry.stat().st_size if entry.is_file() else 0
                entries.append(f"[{kind}] {entry.name} ({size} bytes)")
            return "\n".join(entries) if entries else "(empty directory)"
        except Exception as e:
            return f"Error listing directory: {e}"

    @mcp.tool()
    def file_info(path: str) -> str:
        """Get metadata about a file or directory."""
        import json
        from datetime import datetime
        p = Path(path).resolve()
        if not _is_allowed(p):
            return f"Error: Path not allowed: {path}"
        if not p.exists():
            return f"Error: Path not found: {path}"
        try:
            stat = p.stat()
            info = {
                "path": str(p), "name": p.name,
                "type": "directory" if p.is_dir() else "file",
                "size_bytes": stat.st_size,
                "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                "created": datetime.fromtimestamp(stat.st_ctime).isoformat(),
                "is_symlink": p.is_symlink(),
            }
            return json.dumps(info, indent=2)
        except Exception as e:
            return f"Error getting file info: {e}"
