from pathlib import Path

PROMPTS_DIR = Path(__file__).parent / "prompts"

def _load(name: str) -> str:
    return (PROMPTS_DIR / f"{name}.md").read_text(encoding="utf-8")

TRAVEL_SYSTEM_PROMPT = _load("travel")
VENUE_SYSTEM_PROMPT = _load("venue")
DJ_SYSTEM_PROMPT = _load("dj")