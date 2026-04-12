"""
Agent builder.

Takes an Agent spec (declarative config) and produces a runnable
LangChain/LangGraph agent. This is the only place in the codebase
that knows about ChatOpenAI and create_react_agent — keeps the
LLM-specific concerns out of the agents/ package.
"""
from langchain_core.runnables import Runnable

from langchain_openai import ChatOpenAI

from langchain.agents import create_agent

from wedding_planner.config import OPENAI_API_KEY
from wedding_planner.agents import Agent
from wedding_planner.mcp_clients import get_kiwi_tools
from wedding_planner.tools import WEB_SEARCH_TOOL, playlist_search


# Hardcoded mapping: which agents need MCP tools fetched at build time.
# When an agent's name appears here, the builder fetches the listed
# MCP tools and appends them to the agent's local tools.
#
# Premature to make this configurable — three agents, one mapping entry.
# When this grows beyond ~5 entries, promote it to a tool_sources field
# on the Agent dataclass.
async def _fetch_mcp_tools_for(spec: Agent) -> list:
    if spec.name == "flight":
        return await get_kiwi_tools()
    elif spec.name == "venue":
        return [WEB_SEARCH_TOOL]
    elif spec.name == "dj":
        return [playlist_search]
    return []

async def build_agent(spec: Agent, extra_tools: list | None = None) -> Runnable:
    """
    Build a runnable LangGraph agent from a declarative Agent spec.

    Args:
        spec: The agent spec (name, prompt, model, local tools).
        extra_tools: Additional tools to inject at build time. Used by
            the coordinator to inject sub-agents-as-tools. Local tools
            from the spec and MCP tools (if any) are always included.

    Returns:
        A LangGraph runnable ready to .ainvoke({"messages": [...]}).
    """
    model = ChatOpenAI(
        model=spec.model,
        api_key=OPENAI_API_KEY
    )

    mcp_tools = await _fetch_mcp_tools_for(spec)
    all_tools = [*spec.tools, *mcp_tools, *(extra_tools or [])]
    
    return create_agent(
        model=model,
        tools=all_tools,
        system_prompt=spec.system_prompt
    )