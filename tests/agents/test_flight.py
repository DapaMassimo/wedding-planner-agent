from wedding_planner.agents import Agent
from wedding_planner.agents.flight import FLIGHT_AGENT
from wedding_planner.config import DEFAULT_MODEL


# The exported constant must be an Agent instance.
def test_flight_agent_is_agent_instance():
    assert isinstance(FLIGHT_AGENT, Agent)

# Name must match the expected identifier
def test_flight_agent_name():
    assert FLIGHT_AGENT.name == "flight"

# Description must be a non-empty string
def test_flight_agent_has_description():
    assert isinstance(FLIGHT_AGENT.description, str)

# System prompt must be a non-empty string
def test_flight_agent_has_system_prompt():
    assert isinstance(FLIGHT_AGENT.system_prompt, str)
    assert FLIGHT_AGENT.system_prompt.strip()

# Prompt on the agent must match the actual source file
def test_flight_agent_prompt_matches_source_file():
    from wedding_planner.config import PROMPTS_DIR
    expected = (PROMPTS_DIR / "flight.md").read_text(encoding="utf-8")
    assert FLIGHT_AGENT.system_prompt == expected

# Model must match DEFAULT_MODEL from config
def test_flight_agent_uses_default_model():
    assert FLIGHT_AGENT.model == DEFAULT_MODEL

# Tools must be a list
def test_flight_agent_tools_is_list():
    assert isinstance(FLIGHT_AGENT.tools, list)