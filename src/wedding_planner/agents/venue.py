from wedding_planner.agents.base import Agent
from wedding_planner.prompts_loader import VENUE_SYSTEM_PROMPT
from wedding_planner.config import DEFAULT_MODEL

VENUE_AGENT = Agent(
    name="venue",
    description="Scours the web for wedding venues.",
    system_prompt=VENUE_SYSTEM_PROMPT,
    model=DEFAULT_MODEL,
    tools=[]
)