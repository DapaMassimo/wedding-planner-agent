from pathlib import Path

PROMPTS_DIR = Path(__file__).parent / "prompts"

def _load(name: str) -> str:
    return (PROMPTS_DIR / f"{name}.md").read_text(encoding="utf-8")

FLIGHT_SYSTEM_PROMPT = _load("flight")
VENUE_SYSTEM_PROMPT = _load("venue")
DJ_SYSTEM_PROMPT = _load("dj")
COORDINATOR_SYSTEM_PROMPT = _load("coordinator")