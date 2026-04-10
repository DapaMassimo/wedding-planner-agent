import dataclasses
import pytest

from wedding_planner.agents.base import Agent, Tool

# --- Helper fixtures ---

def _dummy_function(x: int) -> str:
    return str(x)

def _make_tool(**overrides) -> Tool:
    defaults = {
        "name": "test_tool",
        "description": "A test tool",
        "input_schema": {"type": "object", "properties": {}},
        "function": _dummy_function,
    }
    return Tool(**(defaults | overrides))

def _make_agent(**overrides) -> Agent:
    defaults = {
        "name": "test_agent",
        "description": "A test agent.",
        "system_prompt": "You are a test agent.",
        "model": "test-model"
    }
    return Agent(**(defaults | overrides))

# --- Agent instantiation ---

# All fields hsould be stored exactly as passed.
def test_agent_stores_all_fields():
    agent = Agent(
        name="travel",
        description="Handles travel.",
        system_prompt="You are a travel agent.",
        model="o3-mini",
        tools=[]
    )
    assert agent.name == "travel"
    assert agent.description == "Handles travel."
    assert agent.system_prompt == "You are a travel agent."
    assert agent.model == "o3-mini"
    assert agent.tools == []

# Omitting tools should give a fresh empty list, not None or an error.
def test_agent_default_tools_is_empty_list():
    agent = _make_agent()
    assert isinstance(agent.tools, list)
    assert agent.tools == []

# Each instance must get its own list, not a shared reference.
# (default_factory safety -> the classic mutable-default-argument trap.)
def test_agent_default_tools_are_independent():
    a = _make_agent()
    b = _make_agent()
    assert a.tools is not b.tools


# --- Agent is frozen ---

# Assigning to a field after creation must raise.
# Guards against someone removing frozen=True from the dataclass
def test_agent_is_frozen():
    agent = _make_agent()
    with pytest.raises(dataclasses.FrozenInstanceError):
        agent.name = "something_else"

def test_agent_frozen_system_prompt():
    agent = _make_agent()
    with pytest.raises(dataclasses.FrozenInstanceError):
        agent.system_prompt = "new prompt"


# --- Agent equality ---

# Two agents with identical fields should be equal.
def test_agent_equality_same_fields():
    a = _make_agent(name="x")
    b = _make_agent(name="x")
    assert a == b

# Two agents with different fields should not be equal
def test_agent_equality_different_fields():
    a = _make_agent(name="x")
    b = _make_agent(name="y")
    assert a != b

# --- Tool instantiation ---

# All fields should be stored exactly as passed
def test_tool_stores_all_fields():
    schema = {"type": "object", "properties": {"q": {"type": "string"}}}
    tool = Tool(
        name="search",
        description="Searches the web.",
        input_schema=schema,
        function=_dummy_function
    )
    assert tool.name == "search"
    assert tool.description == "Searches the web."
    assert tool.input_schema == schema
    assert tool.function is _dummy_function

# --- Tool is frozen ---

def test_tool_is_frozen():
    tool = _make_tool()
    with pytest.raises(dataclasses.FrozenInstanceError):
        tool.name = "other"

# --- Tool functions accepts any callable

# Regular function
def test_tool_accepts_function():
    tool = _make_tool(function=_dummy_function)
    assert tool.function(42) == "42"

# Lambda
def test_tool_accepts_lambda():
    tool = _make_tool(function=lambda x: x * 2)
    assert tool.function(5) == 10

# Class with __call__
def test_tool_accepts_callable_class():
    class Doubler:
        def __call__(self, x):
            return x*2
    
    tool = _make_tool(function=Doubler())
    assert callable(Doubler)
    assert tool.function(5) == 10

# --- Tool equality ---

def test_tool_equality_same_fields():
    a = _make_tool(name="x")
    b = _make_tool(name="x")
    assert a == b

def test_too_equality_different_fields():
    a = _make_tool(name="x")
    b = _make_tool(name="y")

# --- Agent with tools ---

# Agent should store Tool instances in its tools list
def test_agent_with_tools():
    tool = _make_tool
    agent = _make_agent(tools=[tool])
    assert len(agent.tools) == 1
    assert agent.tools[0] == tool