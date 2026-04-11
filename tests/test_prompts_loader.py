from pathlib import Path

from wedding_planner import prompts_loader

PROMPTS_DIR = Path(prompts_loader.__file__).parent / "prompts"

def _read(name: str) -> str:
    return (PROMPTS_DIR / f"{name}.md").read_text(encoding="utf-8")

# Verify the loaded constant matches the .md file content exactly.
# Catches loader bugs: wrong filename, different encoding, unintended transformations.
def test_travel_agent_prompt_matches_files():
    assert prompts_loader.TRAVEL_SYSTEM_PROMPT == _read("travel")

# Same check for the venue agent.
def test_venue_agent_prompt_matches_files():
    assert prompts_loader.VENUE_SYSTEM_PROMPT == _read("venue")

# Same check for the dj agent.
def test_dj_agent_prompt_matches_files():
    assert prompts_loader.DJ_SYSTEM_PROMPT == _read("dj")

# Same check for the coordinator agent
def test_coordinator_agent_prompt_matches_files():
    assert prompts_loader.COORDINATOR_SYSTEM_PROMPT == _read("coordinator")

# Ensure no prompt is empty or whitespace-only.
# Catches accidentally empty files and the classic `f.read` (without parentheses)
# bug, which would store the method object instead of the file content.
def test_prompts_are_non_empty():
    assert prompts_loader.TRAVEL_SYSTEM_PROMPT.strip()
    assert prompts_loader.VENUE_SYSTEM_PROMPT.strip()
    assert prompts_loader.DJ_SYSTEM_PROMPT.strip()
    assert prompts_loader.COORDINATOR_SYSTEM_PROMPT.strip()

# Type sanity check: constants must be strings, not file objects or methods.
def test_prompts_are_strings():
    assert isinstance(prompts_loader.TRAVEL_SYSTEM_PROMPT, str)
    assert isinstance(prompts_loader.VENUE_SYSTEM_PROMPT, str)
    assert isinstance(prompts_loader.DJ_SYSTEM_PROMPT, str)
    assert isinstance(prompts_loader.COORDINATOR_SYSTEM_PROMPT, str)