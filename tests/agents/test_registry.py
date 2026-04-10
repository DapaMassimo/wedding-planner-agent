from wedding_planner.agents import (
    AGENTS,
    TRAVEL_AGENT,
    VENUE_AGENT,
    DJ_AGENT,
    __all__
)
from wedding_planner.agents.base import Agent

# --- AGENTS dict structure ---

# Registry must contain exactly the expected keys
def test_agents_has_expected_keys():
    assert set(AGENTS.keys()) == {"travel", "venue", "dj"}

# Registry values must be the same objects as the module-level constants
def test_agents_values_are_the_actual_instances():
    expected = {
        "travel": TRAVEL_AGENT,
        "venue": VENUE_AGENT,
        "dj": DJ_AGENT,
    }
    assert len(AGENTS) == len(expected), f"AGENTS has {len(AGENTS)} entries, expected {len(expected)}"
    for key, expected_agent in expected.items():
        assert AGENTS[key] is expected_agent, f"AGENTS['{key}'] is not the expected instance"

# --- Uniqueness ---

# No two agents should share a name. Catches copy-paste errors
def test_agent_names_are_unique():
    names = [agent.name for agent in AGENTS.values()]
    assert len(names) == len(set(names))

# --- __all__ ---

# __all__ must contain exactly these symbols — no more, no less.
def test_all_contains_exactly_expected_names():
    assert set(__all__) == {"TRAVEL_AGENT", "VENUE_AGENT", "DJ_AGENT", "AGENTS"}

# --- Catch-all validation (scales when you add agent) ---

# Every agent in the registry must have non-empty core fields
def test_all_agents_have_required_fields():
    for name, agent in AGENTS.items():
        assert agent.name, f"{name}: name is empty"
        assert agent.description, f"{name}: description is empty"
        assert agent.model, f"{name}: model is empty"
        assert agent.system_prompt, f"{name}: system prompt is empty"
        assert isinstance(agent.tools, list), f"{name}: tools is not a list!"

# Registry keys must match the agent's own name field.
def test_registry_keys_match_agent_names():
    for key, agent in AGENTS.items():
        assert key == agent.name, f"Key '{key}' doesn't match agent.name '{agent.name}'"