from wedding_planner.agents import (
    AGENTS,
    FLIGHT_AGENT,
    VENUE_AGENT,
    COORDINATOR_AGENT,
    DJ_AGENT,
    __all__,
)

# --- AGENTS dict structure ---

# Registry must contain exactly the expected keys
def test_agents_has_expected_keys():
    assert set(AGENTS.keys()) == {"flight", "venue", "dj", "coordinator"}

# Registry values must be the same objects as the module-level constants
def test_agents_values_are_the_actual_instances():
    expected = {
        "flight": FLIGHT_AGENT,
        "venue": VENUE_AGENT,
        "dj": DJ_AGENT,
        "coordinator": COORDINATOR_AGENT,
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
    assert set(__all__) == {"Agent", "FLIGHT_AGENT", "VENUE_AGENT", "DJ_AGENT", "COORDINATOR_AGENT", "AGENTS"}

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
