"""Web fetch tools for MCP Server Toolkit."""

from mcp.server.fastmcp import FastMCP


def register_web_fetch_tools(mcp: FastMCP, config: dict) -> None:
    """Register web fetch tools with the MCP server."""
    timeout = config.get("timeout", 30)
    max_size = config.get("max_response_size", 1048576)
    follow = config.get("follow_redirects", True)
    user_agent = config.get("user_agent", "MCP-Server-Toolkit/1.0")

    @mcp.tool()
    def fetch_url(url: str, method: str = "GET", headers: dict = None) -> str:
        """Fetch content from a URL using HTTP."""
        import httpx
        try:
            with httpx.Client(timeout=timeout, follow_redirects=follow, headers={"User-Agent": user_agent, **(headers or {})}) as client:
                response = client.request(method.upper(), url)
                if len(response.content) > max_size:
                    return f"Error: Response too large ({len(response.content)} bytes, max {max_size})"
                parts = [f"Status: {response.status_code}"]
                ct = response.headers.get("content-type", "")
                parts.append(f"Content-Type: {ct}")
                if "json" in ct:
                    import json
                    parts.append(json.dumps(response.json(), indent=2))
                else:
                    parts.append(response.text[:max_size])
                return "\n".join(parts)
        except httpx.TimeoutException:
            return f"Error: Request timed out after {timeout}s"
        except httpx.RequestError as e:
            return f"Error: Request failed: {e}"
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool()
    def post_json(url: str, data: dict, headers: dict = None) -> str:
        """POST JSON data to a URL."""
        import httpx
        try:
            with httpx.Client(timeout=timeout, follow_redirects=follow, headers={"User-Agent": user_agent, **(headers or {})}) as client:
                response = client.post(url, json=data)
                return f"Status: {response.status_code}\n\n{response.text[:max_size]}"
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool()
    def check_url_status(url: str) -> str:
        """Check if a URL is reachable and return its status."""
        import httpx, time
        try:
            start = time.monotonic()
            with httpx.Client(timeout=timeout, follow_redirects=follow, headers={"User-Agent": user_agent}) as client:
                response = client.head(url)
                elapsed = (time.monotonic() - start) * 1000
                return f"Status: {response.status_code}\nTime: {elapsed:.0f}ms\nContent-Type: {response.headers.get('content-type', 'N/A')}"
        except Exception as e:
            return f"Error: {e}"
