from dataclasses import dataclass, field
from wedding_planner.tools import Tool 


@dataclass(frozen=True)
class Agent:
    name: str
    description: str
    system_prompt: str
    model: str
    tools: list[Tool] = field(default_factory=list)
