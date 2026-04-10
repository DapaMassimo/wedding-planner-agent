from wedding_planner.agents.base import Agent
from wedding_planner.prompts_loader import DJ_SYSTEM_PROMPT
from wedding_planner.config import DEFAULT_MODEL

DJ_AGENT = Agent(
    name="dj",
    description="Queries music DB looking for a wedding appropriate playlist",
    system_prompt=DJ_SYSTEM_PROMPT,
    model=DEFAULT_MODEL,
    tools=[]
)