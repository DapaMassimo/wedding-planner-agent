"""
MCP client for the Kiwi.com flight search server.

Connects to Kiwi's hosted MCP endpoint and exposes its tools as
LangChain BaseTool instances, ready to be passed into an agent's
tool list. The flight agent uses this to search flights without
us having to write our own flight API integration.
"""
from langchain_core.tools import BaseTool
from langchain_mcp_adapters.client import MultiServerMCPClient

KIWI_MCP_URL = "https://mcp.kiwi.com"
KIWI_SERVER_NAME = "kiwi"

def _build_client() -> MultiServerMCPClient:
    return MultiServerMCPClient(
        connections={
            KIWI_SERVER_NAME: {
                "url": KIWI_MCP_URL,
                "transport": "streamable_http"
            }
        }
    )

async def get_kiwi_tools() -> list[BaseTool]:
    """
    Opens a sessions to Kiwi's MCP server and
    return its tools as LangChain BaseTool instances.

    Each call creates a new client.
    """
    client = _build_client()
    return await client.get_tools()