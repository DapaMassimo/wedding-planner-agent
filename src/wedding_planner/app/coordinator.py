"""
Coordinator agent builder.

Builds the three sub-agents (flight, venue, dj), wraps each one as
a LangChain tool, and then builds the coordinator agent with those
wrapped tools as its only capabilities. The coordinator's LLM picks
which sub-agent to delegate to based on the user's request.
"""
from langchain_core.runnables import Runnable
from langchain_core.messages import HumanMessage

from langchain_core.tools import BaseTool, StructuredTool

from wedding_planner.agents import (
    Agent,
    AGENTS,
    COORDINATOR_AGENT
)
from wedding_planner.app.builder import build_agent


def _agent_to_tool(spec: Agent, runnable: Runnable) -> BaseTool:
    """
    Wrap a runnable agent as a LangChain tool the coordinator can call.

    The tool name and description are derived from the agent spec, so
    the coordinator's LLM sees consistent metadata: the same name and
    description we declared in agents/<name>.py.
    """
    tool_name = f"call_{spec.name}_agent"
    tool_description = spec.description

    async def _delegate(query: str) -> str:
        """Delegate a self-contained query to the wrapped sub-agent"""
        result = await runnable.ainvoke(
            {"messages": [HumanMessage(content=query)]}
        )
        # The runnable returns a state dict with a `messages` list;
        # the last message is the agent't final reply
        return result["messages"][-1].content
    
    return StructuredTool.from_function(
        coroutine=_delegate,
        name=tool_name,
        description=tool_description
    )

async def build_coordinator() -> Runnable:
    """
    Build the full coordinator agent with all three sub-agents wrapped
    as tools. Returns a runnable ready to .ainvoke.
    """
    sub_agent_tools: list[BaseTool] = []
    for spec in AGENTS.values():
        runnable = await build_agent(spec)
        sub_agent_tools.append(_agent_to_tool(spec, runnable))
    
    return await build_agent(COORDINATOR_AGENT, extra_tools=sub_agent_tools)