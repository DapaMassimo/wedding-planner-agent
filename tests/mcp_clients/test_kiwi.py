import pytest
from unittest.mock import AsyncMock, patch

from wedding_planner.mcp_clients.kiwi import (
    KIWI_MCP_URL,
    KIWI_SERVER_NAME,
    _build_client,
    get_kiwi_tools
)


# --- Configuration constants ---

def test_kiwi_url_is_correct():
    assert KIWI_MCP_URL == "https://mcp.kiwi.com"


def test_kiwi_server_name():
    assert KIWI_SERVER_NAME == "kiwi"

# --- Build client ---

def test_build_client_uses_expected_connection():
    client = _build_client()
    assert KIWI_SERVER_NAME in client.connections
    conn = client.connections[KIWI_SERVER_NAME]
    url = conn.get("url") if isinstance(conn, dict) else conn.url
    transport = conn.get("transport") if isinstance(conn, dict) else conn.transport
    assert url == KIWI_MCP_URL
    assert transport == "streamable_http"

# --- get_kiwi_tools() ---

# Verify get_kiwi_tools delegates to MultiServerMCPClient.get_tools
# without hitting the real network. Patch the method on the class so
# the instance built inside _build_client picks up the mock
@pytest.mark.asyncio
async def test_get_kiwi_tools_returns_client_tools():
    fake_tools = ["fake_tool_a", "fake_tool_b"]
    with patch(
        "wedding_planner.mcp_clients.kiwi.MultiServerMCPClient.get_tools",
        new=AsyncMock(return_value=fake_tools)
    ) as mock_get:
        result = await get_kiwi_tools()
        mock_get.assert_awaited_once()
        assert result == fake_tools