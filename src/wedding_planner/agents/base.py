from dataclasses import dataclass, field

from langchain_core.tools import BaseTool


@dataclass(frozen=True)
class Agent:
    """Declarative spec for an agent.

    This is internal config — the actual runnable agent is built
    later by the agent builder, which combines this spec with an
    LLM client and any tools fetched from MCP servers.
    """
    name: str
    description: str
    system_prompt: str
    model: str
    tools: list[BaseTool] = field(default_factory=list)
