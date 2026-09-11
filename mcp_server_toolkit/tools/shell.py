"""Shell command tools for MCP Server Toolkit."""

import subprocess
from pathlib import Path
from mcp.server.fastmcp import FastMCP


def register_shell_tools(mcp: FastMCP, config: dict) -> None:
    """Register shell tools with the MCP server."""
    allowed_commands = config.get("allowed_commands", [])
    blocked_commands = config.get("blocked_commands", ["rm -rf /", "dd", "mkfs"])
    timeout = config.get("timeout", 60)
    work_dir = config.get("working_directory", ".")

    def _is_blocked(cmd: str) -> bool:
        cmd_lower = cmd.lower().strip()
        return any(b.lower() in cmd_lower for b in blocked_commands)

    def _is_allowed(cmd: str) -> bool:
        if not allowed_commands:
            return True
        return cmd.strip().split()[0] in allowed_commands

    @mcp.tool()
    def run_command(command: str, cwd: str = None) -> str:
        """Execute a shell command and return its output."""
        if _is_blocked(command):
            return f"Error: Command blocked for safety: {command}"
        if not _is_allowed(command):
            return f"Error: Command not in allowed list: {command.strip().split()[0]}"
        effective_cwd = cwd or work_dir
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=timeout, cwd=effective_cwd)
            parts = []
            if result.stdout:
                parts.append(f"STDOUT:\n{result.stdout}")
            if result.stderr:
                parts.append(f"STDERR:\n{result.stderr}")
            parts.append(f"Exit code: {result.returncode}")
            return "\n\n".join(parts) if parts else "(no output)"
        except subprocess.TimeoutExpired:
            return f"Error: Command timed out after {timeout}s"
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool()
    def run_python(code: str) -> str:
        """Execute Python code in a subprocess and return the output."""
        if _is_blocked(code):
            return "Error: Code blocked for safety."
        try:
            result = subprocess.run(["python3", "-c", code], capture_output=True, text=True, timeout=timeout, cwd=work_dir)
            parts = []
            if result.stdout:
                parts.append(result.stdout)
            if result.stderr:
                parts.append(f"STDERR:\n{result.stderr}")
            parts.append(f"Exit code: {result.returncode}")
            return "\n".join(parts) if parts else "(no output)"
        except subprocess.TimeoutExpired:
            return f"Error: Code timed out after {timeout}s"
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool()
    def check_command_exists(command: str) -> str:
        """Check if a command is available on the system."""
        import shutil
        path = shutil.which(command)
        if path:
            return f"'{command}' found at: {path}"
        return f"'{command}' not found in PATH"
