from pathlib import Path

from wedding_planner.agents import AGENTS
from wedding_planner.agents.base import Agent
from wedding_planner.config import DEFAULT_MODEL, PROMPTS_DIR


# --- Full import chain ---

# If this test runs at all, the entire import chain works:
# config.py -> prompts_loader.py -> agents/*.py -> agents/__init__.py
# A failure here means something fundamental is broken.
def test_full_import_chain():
    assert AGENTS is not None
    assert len(AGENTS) > 0


# --- Agent prompts match their source files ---

# Verify each agent's system_prompt matches the actual .md file.
# Different from test_prompts_loader (which tests the loader constants)
# and from test_flight/venue/dj (which test individual agents).
# This catches the case where an agent imports the WRONG constant
# from prompts_loader — e.g. flight.py accidentally uses DJ_SYSTEM_PROMPT.
def test_flight_agent_prompt_matches_source():
    expected = (PROMPTS_DIR / "flight.md").read_text(encoding="utf-8")
    assert AGENTS["flight"].system_prompt == expected


def test_venue_agent_prompt_matches_source():
    expected = (PROMPTS_DIR / "venue.md").read_text(encoding="utf-8")
    assert AGENTS["venue"].system_prompt == expected


def test_dj_agent_prompt_matches_source():
    expected = (PROMPTS_DIR / "dj.md").read_text(encoding="utf-8")
    assert AGENTS["dj"].system_prompt == expected


# --- Cross-agent invariants ---

# No two agents should share a name.
# Unlike the registry test (which checks dict keys), this checks
# the .name field on the actual Agent objects — catches the case
# where someone adds an agent with a unique dict key but
# copy-pastes the same name= value inside the Agent constructor.
def test_no_duplicate_agent_names():
    names = [agent.name for agent in AGENTS.values()]
    assert len(names) == len(set(names)), f"Duplicate names found: {names}"


# All agents must use a non-empty model string.
def test_all_agents_have_a_model():
    for name, agent in AGENTS.items():
        assert agent.model, f"{name}: model is empty"


# All agents currently use DEFAULT_MODEL.
# Remove this test if agents start using different models intentionally.
def test_all_agents_use_default_model():
    for name, agent in AGENTS.items():
        assert agent.model == DEFAULT_MODEL, (
            f"{name}: expected model '{DEFAULT_MODEL}', got '{agent.model}'"
        )


# Every prompt file in prompts/ should have a corresponding agent.
# Catches orphaned prompt files (someone wrote a prompt but forgot
# to create the agent) and missing prompts (agent exists but no file).
def test_prompt_files_match_agents():
    prompt_files = {p.stem for p in PROMPTS_DIR.glob("*.md")}
    agent_names = set(AGENTS.keys())
    assert prompt_files == agent_names, (
        f"Mismatch — prompt files: {prompt_files}, agents: {agent_names}"
    )
