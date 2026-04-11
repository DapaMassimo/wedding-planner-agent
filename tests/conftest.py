import pytest
from wedding_planner.agents import Agent
from wedding_planner.tools import Tool

# --- Helper fixtures ---

@pytest.fixture
def make_agent():
    def _make(**overrides) -> Agent:
        defaults = {
            "name": "test_agent",
            "description": "A test agent.",
            "system_prompt": "You are a test agent.",
            "model": "test-model"
        }
        return Agent(**(defaults | overrides))
    return _make

@pytest.fixture
def dummy_function():
    def _dummy(x: int) -> str:
        return str(x)
    return _dummy

@pytest.fixture
def make_tool(dummy_function):
    def _make(**overrides) -> Tool:
        defaults = {
            "name": "test_tool",
            "description": "A test tool",
            "input_schema": {"type": "object", "properties": {}},
            "function": dummy_function,
        }
        return Tool(**(defaults | overrides))
    return _make

