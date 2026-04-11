import pytest
from langchain_core.tools import BaseTool, StructuredTool

from wedding_planner.agents import Agent

# --- Helper fixtures ---

@pytest.fixture
def make_agent():
    def _make(**overrides) -> Agent:
        defaults = {
            "name": "test_agent",
            "description": "A test agent.",
            "system_prompt": "You are a test agent.",
            "model": "test-model",
        }
        return Agent(**(defaults | overrides))
    return _make


@pytest.fixture
def make_tool():
    def _make(**overrides) -> BaseTool:
        defaults = {
            "name": "test_tool",
            "description": "A test tool.",
            "func": lambda x: str(x),
        }
        return StructuredTool.from_function(**(defaults | overrides))
    return _make
