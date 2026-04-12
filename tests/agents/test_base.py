import dataclasses
import pytest

from wedding_planner.agents import Agent

# --- Agent instantiation ---

# All fields hsould be stored exactly as passed.
def test_agent_stores_all_fields():
    agent = Agent(
        name="flight",
        description="Handles flights.",
        system_prompt="You are a flight agent.",
        model="o3-mini",
        tools=[]
    )
    assert agent.name == "flight"
    assert agent.description == "Handles flights."
    assert agent.system_prompt == "You are a flight agent."
    assert agent.model == "o3-mini"
    assert agent.tools == []

# Omitting tools should give a fresh empty list, not None or an error.
def test_agent_default_tools_is_empty_list(make_agent):
    agent = make_agent()
    assert isinstance(agent.tools, list)
    assert agent.tools == []

# Each instance must get its own list, not a shared reference.
# (default_factory safety -> the classic mutable-default-argument trap.)
def test_agent_default_tools_are_independent(make_agent):
    a = make_agent()
    b = make_agent()
    assert a.tools is not b.tools


# --- Agent is frozen ---

# Assigning to a field after creation must raise.
# Guards against someone removing frozen=True from the dataclass
def test_agent_is_frozen(make_agent):
    agent = make_agent()
    with pytest.raises(dataclasses.FrozenInstanceError):
        agent.name = "something_else"

def test_agent_frozen_system_prompt(make_agent):
    agent = make_agent()
    with pytest.raises(dataclasses.FrozenInstanceError):
        agent.system_prompt = "new prompt"


# --- Agent equality ---

# Two agents with identical fields should be equal.
def test_agent_equality_same_fields(make_agent):
    a = make_agent(name="x")
    b = make_agent(name="x")
    assert a == b

# Two agents with different fields should not be equal
def test_agent_equality_different_fields(make_agent):
    a = make_agent(name="x")
    b = make_agent(name="y")
    assert a != b

# --- Agent with tools ---

# Agent should store BaseTool instances in its tools list.
def test_agent_with_tools(make_tool, make_agent):
    tool = make_tool()
    agent = make_agent(tools=[tool])
    assert len(agent.tools) == 1
    assert agent.tools[0] is tool