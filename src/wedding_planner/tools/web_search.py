"""
Web search tool backed by Tavily, exposed as a LangChain tool.

Used by agents that need fresh information from the public web
(venue prices, current availability, recent reviews, etc.).
"""
from langchain_tavily import TavilySearch

from wedding_planner.config import TAVILY_API_KEY

WEB_SEARCH_TOOL = TavilySearch(
    max_results=5,
    topic="general",
    tavily_api_key=TAVILY_API_KEY
)