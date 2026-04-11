from .base import Agent
from wedding_planner.prompts_loader import COORDINATOR_SYSTEM_PROMPT
from wedding_planner.config import DEFAULT_MODEL

COORDINATOR_AGENT = Agent(
    name="coordinator",
    description="Top-level orchestrator that delegates wedding planning tasks to specialized sub-agents.",
    system_prompt=COORDINATOR_SYSTEM_PROMPT,
    model=DEFAULT_MODEL,
    tools=[]
)