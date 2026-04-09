from wedding_planner.agents.base import Agent
from wedding_planner.prompts_loader import TRAVEL_SYSTEM_PROMPT
from wedding_planner.config import DEFAULT_MODEL

TRAVEL_AGENT = Agent(
    name="travel",
    description="Handles flights travel logistics for guests.",
    system_prompt=TRAVEL_SYSTEM_PROMPT,
    model=DEFAULT_MODEL,
    tools=[]
)