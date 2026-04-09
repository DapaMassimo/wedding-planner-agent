from pathlib import Path

PROMPTS_DIR = Path(__file__).parent / "prompts"

def _load(name: str) -> str:
    return (PROMPTS_DIR / f"{name}.md").read_text(encoding="utf-8")

TRAVEL_SYSTEM_PROMPT = _load("travel-agent")
VENUE_SYSTEM_PROMPT = _load("venue-agent")
DJ_SYSTEM_PROMPT = _load("dj-agent")

print(TRAVEL_SYSTEM_PROMPT)
print(VENUE_SYSTEM_PROMPT)
print(DJ_SYSTEM_PROMPT)