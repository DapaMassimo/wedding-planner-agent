"""Tests for the Tavily-backed web search tool"""
from unittest.mock import patch

from langchain_tavily import TavilySearch

from wedding_planner.tools.web_search import WEB_SEARCH_TOOL


# The exported constant must be a LangChain TavilySearch instance,
# not a different tool wrapper or a None.
def test_web_search_tool_is_tavily_search_instance():
    assert isinstance(WEB_SEARCH_TOOL, TavilySearch)


# The tool must have a non-empty name and description
def test_web_search_tool_has_name_and_description():
    assert WEB_SEARCH_TOOL.name
    assert WEB_SEARCH_TOOL.description
    assert isinstance(WEB_SEARCH_TOOL.name, str)
    assert isinstance(WEB_SEARCH_TOOL.description, str)


# The tool must declare an input schema so the LLM knows what to pass
def test_web_search_tool_has_input_schema():
    schema = WEB_SEARCH_TOOL.args_schema
    assert schema is not None


# Configuration default matches expected
def test_web_search_too_max_results_default():
    assert WEB_SEARCH_TOOL.max_results == 5

# Tool must have an api key set
def test_web_search_tool_has_api_key():
    assert WEB_SEARCH_TOOL.api_wrapper.tavily_api_key is not None



# Integration test with patched response
def test_web_search_tool_invokes_underlying_client():
    fake_response = {
        "results": [
            {"title": "Test", "url": "https://example.com", "content": "stub"}
        ]
    }
    # Patch the method on the client class
    with patch(
        "langchain_tavily._utilities.TavilySearchAPIWrapper.raw_results",
        return_value=fake_response
    ) as mock_call:
        result = WEB_SEARCH_TOOL.invoke({"query": "test query"})
        mock_call.assert_called_once()
        assert result is not None