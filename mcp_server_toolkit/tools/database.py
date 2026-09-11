"""Database tools for MCP Server Toolkit."""

from mcp.server.fastmcp import FastMCP


def register_database_tools(mcp: FastMCP, config: dict) -> None:
    """Register database tools with the MCP server."""
    connection_string = config.get("connection_string", "sqlite:///data.db")
    pool_size = config.get("pool_size", 5)
    max_overflow = config.get("max_overflow", 10)

    def _get_engine():
        from sqlalchemy import create_engine
        return create_engine(connection_string, pool_size=pool_size, max_overflow=max_overflow, pool_pre_ping=True)

    @mcp.tool()
    def execute_query(sql: str, params: dict = None) -> str:
        """Execute a SQL query and return results."""
        import json
        from sqlalchemy import text
        try:
            engine = _get_engine()
            with engine.connect() as conn:
                result = conn.execute(text(sql), params or {})
                if result.returns_rows:
                    columns = list(result.keys())
                    rows = [dict(zip(columns, row)) for row in result.fetchmany(100)]
                    if not rows:
                        return "Query returned 0 rows."
                    return json.dumps({"columns": columns, "row_count": len(rows), "rows": rows}, indent=2, default=str)
                else:
                    conn.commit()
                    return f"Query executed. Rows affected: {result.rowcount}"
        except Exception as e:
            return f"Database error: {e}"

    @mcp.tool()
    def list_tables() -> str:
        """List all tables in the database."""
        from sqlalchemy import inspect
        try:
            engine = _get_engine()
            inspector = inspect(engine)
            tables = inspector.get_table_names()
            if not tables:
                return "No tables found in the database."
            lines = []
            for table in tables:
                cols = inspector.get_columns(table)
                lines.append(f"- {table} ({len(cols)} columns): {', '.join(c['name'] for c in cols)}")
            return "\n".join(lines)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool()
    def describe_table(table_name: str) -> str:
        """Get the schema of a specific table."""
        import json
        from sqlalchemy import inspect
        try:
            engine = _get_engine()
            inspector = inspect(engine)
            if table_name not in inspector.get_table_names():
                return f"Error: Table '{table_name}' not found."
            columns = inspector.get_columns(table_name)
            pk = inspector.get_pk_constraint(table_name)
            fks = inspector.get_foreign_keys(table_name)
            result = {
                "table": table_name,
                "primary_key": pk.get("constrained_columns", []),
                "columns": [{"name": c["name"], "type": str(c["type"]), "nullable": c.get("nullable", True)} for c in columns],
                "foreign_keys": [{"columns": fk["constrained_columns"], "references_table": fk["referred_table"], "references_columns": fk["referred_columns"]} for fk in fks],
            }
            return json.dumps(result, indent=2)
        except Exception as e:
            return f"Error: {e}"
