from pathlib import Path
from wedding_planner.agents.base import Agent
from wedding_planner.agents.dj import DJ_AGENT
from wedding_planner.config import DEFAULT_MODEL

# The exported constant must be an Agent instance.
def test_dj_agent_is_agent_instance():
    assert isinstance(DJ_AGENT, Agent)

# Name must match the expected identifier
def test_dj_agent_name():
    assert DJ_AGENT.name == "dj"

# Description must be a non-empty string
def test_dj_agent_has_description():
    assert isinstance(DJ_AGENT.description, str)

# System prompt must be a non-empty string
def test_dj_agent_has_system_prompt():
    assert isinstance(DJ_AGENT.system_prompt, str)
    assert DJ_AGENT.system_prompt.strip()

# Prompt on the agent must match the actual source file
def test_dj_agent_prompt_matches_source_file():
    from wedding_planner.config import PROMPTS_DIR
    expected = (PROMPTS_DIR / "dj.md").read_text(encoding="utf-8")
    assert DJ_AGENT.system_prompt == expected

# Model must match DEFAULT_MODEL from config
def test_dj_agent_uses_default_model():
    assert DJ_AGENT.model == DEFAULT_MODEL

# Tools must be a list
def test_dj_agent_tools_is_list():
    assert isinstance(DJ_AGENT.tools, list)
    