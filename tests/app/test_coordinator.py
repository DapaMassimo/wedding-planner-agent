"""Tests for the coordinator builder and agent-as-tool wrapping."""
from unittest.mock import AsyncMock, MagicMock, patch

from langchain_core.runnables import Runnable
from langchain_core.messages import HumanMessage
from langchain_core.tools import BaseTool

from wedding_planner.agents import (
    AGENTS,
    COORDINATOR_AGENT,
    DJ_AGENT,
    TRAVEL_AGENT,
    VENUE_AGENT,
)
from wedding_planner.app.coordinator import _agent_to_tool, build_coordinator


# --- _agent_to_tool: name and description match the spec ---
def test_agent_to_tool_name_matches_spec():
    fake_runnable = MagicMock(spec=Runnable)
    for spec in AGENTS.values():
        tool = _agent_to_tool(spec, fake_runnable)
        assert tool.name == f"call_{spec.name}_agent", (
            f"{spec.name}: tool name must match spec.name"
        )


# The wrapped tool's description must come straight from the spec.
# This is what the coordinator's LLM uses to decide when to delegate.
def test_agent_to_tool_description_matches_spec():
    fake_runnable = MagicMock(spec=Runnable)
    for spec in AGENTS.values():
        tool = _agent_to_tool(spec, fake_runnable)
        assert tool.description == spec.description, (
            f"{spec.name}: tool description must match spec.description"
        )


# Wrapped tool must be a BaseTool.
def test_agent_to_tool_returns_basetool():
    fake_runnable = MagicMock(spec=Runnable)
    tool = _agent_to_tool(TRAVEL_AGENT, fake_runnable)
    assert isinstance(tool, BaseTool)


# Invoking the wrapped tool must call the wrapped runnable's ainvoke
# with the query as the user message, and return the last message content.
async def test_agent_to_tool_delegates_to_runnable():
    fake_runnable = MagicMock(spec=Runnable)
    fake_message = MagicMock()
    fake_message.content = "the answer"
    fake_runnable.ainvoke = AsyncMock(return_value={"messages": [fake_message]})

    tool = _agent_to_tool(TRAVEL_AGENT, fake_runnable)
    result = await tool.ainvoke({"query": "find me a flight"})

    assert result == "the answer"
    fake_runnable.ainvoke.assert_awaited_once()
    call_kwargs = fake_runnable.ainvoke.call_args.args[0]
    original_query: HumanMessage = call_kwargs["messages"][0]
    assert original_query.content == "find me a flight"


# --- build_coordinator ---

# Building the coordinator must produce a runnable. The sub-agents are
# all built first (one per AGENTS entry), each gets wrapped as a tool,
# and the coordinator is built with those tools injected.
async def test_build_coordinator_returns_runnable():
    fake_sub_runnable = MagicMock(spec=Runnable)
    fake_coordinator_runnable = MagicMock(spec=Runnable)

    # build_agent is called once per sub-agent, then once for the coordinator.
    # Return the sub_runnable for the first len(AGENTS) calls, then the
    # coordinator_runnable for the final call.
    return_sequence = (
        [fake_sub_runnable] * len(AGENTS) + [fake_coordinator_runnable]
    )

    with patch(
        "wedding_planner.app.coordinator.build_agent",
        new=AsyncMock(side_effect=return_sequence),
    ) as mock_build:
        result = await build_coordinator()

    assert result is fake_coordinator_runnable
    # Once per sub-agent + once for the coordinator.
    assert mock_build.await_count == len(AGENTS) + 1

    # The last call is the coordinator build, with extra_tools containing
    # one wrapped tool per sub-agent.
    last_call = mock_build.await_args_list[-1]
    assert last_call.args[0] is COORDINATOR_AGENT
    extra_tools = last_call.kwargs["extra_tools"]
    assert len(extra_tools) == len(AGENTS)
    tool_names = {t.name for t in extra_tools}
    expected_names = {f"call_{name}_agent" for name in AGENTS.keys()}
    assert tool_names == expected_names
