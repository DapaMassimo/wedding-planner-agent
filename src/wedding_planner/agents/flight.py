from wedding_planner.agents.base import Agent
from wedding_planner.prompts_loader import FLIGHT_SYSTEM_PROMPT
from wedding_planner.config import DEFAULT_MODEL

FLIGHT_AGENT = Agent(
    name="flight",
    description="Searches for flights given an origin, destination, and date. Uses the Kiwi MCP server to find real flight options.",
    system_prompt=FLIGHT_SYSTEM_PROMPT,
    model=DEFAULT_MODEL,
    tools=[],
)