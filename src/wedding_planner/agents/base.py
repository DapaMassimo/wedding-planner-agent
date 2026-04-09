from dataclasses import dataclass, field
from typing import Any,Callable

@dataclass(frozen=True)
class Agent:
    name: str
    description: str
    system_prompt: str
    model: str

@dataclass(frozen=True)
class Tool:
    """A callable capability an agent can invoke.
    
    Attributes:
        name: Unique identifier the LLM uses to call this tool.
        description: Natural-language explanation of what the tool does and when to use it.
        input_schema: JSON Schema describing the tool's parameter.
            The LLM uses this to format arguments correctly.
        function: The actual Python callable that runs when invoked.
            Receives the parsed arguments as keyword args, returns a result.
    """
    name: str
    description: str
    input_schema: dict[str, Any]
    function: Callable[..., Any]
