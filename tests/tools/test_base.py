import pytest
import dataclasses

from wedding_planner.tools import Tool

# --- Tool instantiation ---

# All fields should be stored exactly as passed
def test_tool_stores_all_fields(dummy_function):
    schema = {"type": "object", "properties": {"q": {"type": "string"}}}
    tool = Tool(
        name="search",
        description="Searches the web.",
        input_schema=schema,
        function=dummy_function
    )
    assert tool.name == "search"
    assert tool.description == "Searches the web."
    assert tool.input_schema == schema
    assert tool.function is dummy_function

# --- Tool is frozen ---

def test_tool_is_frozen(make_tool):
    tool = make_tool()
    with pytest.raises(dataclasses.FrozenInstanceError):
        tool.name = "other"

# --- Tool functions accepts any callable

# Regular function
def test_tool_accepts_function(make_tool, dummy_function):
    tool = make_tool(function=dummy_function)
    assert tool.function(42) == "42"

# Lambda
def test_tool_accepts_lambda(make_tool):
    tool = make_tool(function=lambda x: x * 2)
    assert tool.function(5) == 10

# Class with __call__
def test_tool_accepts_callable_class(make_tool):
    class Doubler:
        def __call__(self, x):
            return x*2
    
    tool = make_tool(function=Doubler())
    assert callable(Doubler)
    assert tool.function(5) == 10

# --- Tool equality ---

def test_tool_equality_same_fields(make_tool):
    a = make_tool(name="x")
    b = make_tool(name="x")
    assert a == b

def test_too_equality_different_fields(make_tool):
    a = make_tool(name="x")
    b = make_tool(name="y")
