"""Tests for the agent builder."""
from unittest.mock import AsyncMock, MagicMock, patch

from langchain_core.runnables import Runnable

from wedding_planner.tools import WEB_SEARCH_TOOL
from wedding_planner.agents import FLIGHT_AGENT, VENUE_AGENT, DJ_AGENT, Agent
from wedding_planner.app.builder import build_agent, _fetch_mcp_tools_for


# --- _fetch_mcp_tools_for ---

# Flight agent must trigger Kiwi MCP tool fetching.
async def test_fetch_mcp_tools_for_flight_calls_kiwi():
    fake_tools = [MagicMock(name="kiwi_tool_a"), MagicMock(name="kiwi_tool_b")]
    with patch(
        "wedding_planner.app.builder.get_kiwi_tools",
        new=AsyncMock(return_value=fake_tools),
    ) as mock_get:
        result = await _fetch_mcp_tools_for(FLIGHT_AGENT)
        mock_get.assert_awaited_once()
        assert result == fake_tools

# Venue agent must return WEB_SEARCH_TOOL.
async def test_fetch_mcp_tools_for_venue():
    result = await _fetch_mcp_tools_for(VENUE_AGENT)
    assert result == [WEB_SEARCH_TOOL]

# DJ agent must return WEB_SEARCH_TOOL.
async def test_fetch_mcp_tools_for_dj():
    result = await _fetch_mcp_tools_for(DJ_AGENT)
    assert result == [WEB_SEARCH_TOOL]

# Non-flight, non-venue, non-dj agents must not fetch any MCP tools.
async def test_fetch_mcp_tools_for_unknown_returns_empty(make_agent):
    result = await _fetch_mcp_tools_for(make_agent())
    assert result == []


# --- build_agent ---

# build_agent must return a Runnable.
async def test_build_agent_returns_runnable(make_agent):
    agent = await build_agent(make_agent())
    assert isinstance(agent, Runnable)


# Verifies the builder passes the spec's prompt and tools through to
# create_agent. Patches create_agent so the LLM is never
# actually instantiated.
async def test_build_agent_passes_spec_to_create_agent():
    fake_runnable = MagicMock(spec=Runnable)
    with patch(
        "wedding_planner.app.builder.get_kiwi_tools",
        new=AsyncMock(return_value=[]),
    ), patch(
        "wedding_planner.app.builder.create_agent",
        return_value=fake_runnable,
    ) as mock_create:
        result = await build_agent(FLIGHT_AGENT)
        assert result is fake_runnable
        mock_create.assert_called_once()
        kwargs = mock_create.call_args.kwargs
        assert kwargs["system_prompt"] == FLIGHT_AGENT.system_prompt
        assert kwargs["tools"] == list(FLIGHT_AGENT.tools)
