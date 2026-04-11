import os
import importlib
import pytest

from wedding_planner.config import (
    _required,
    DEFAULT_MODEL,
    ROUTER_MODEL,
    DEFAULT_MAX_TOKENS,
    DEFAULT_TEMPERATURE,
    PACKAGE_ROOT,
    PROMPTS_DIR
)

# --- _required() tests ---

# Raises RuntimeError with the variable name when the env var is missing
def test_required_raises_when_missing(monkeypatch):
    monkeypatch.delenv("FAKE_VAR", raising=False)
    with pytest.raises(RuntimeError, match="FAKE_VAR"):
        _required("FAKE_VAR")

# Returns the value when the env var is present.
def test_required_returns_value_when_set(monkeypatch):
    monkeypatch.setenv("FAKE_VAR", "hello")
    assert _required("FAKE_VAR") == "hello"

# Empty string should also be treated as missing
def test_required_raises_on_empty_string(monkeypatch):
    monkeypatch.setenv("FAKE_VAR", "")
    with pytest.raises(RuntimeError, match="FAKE_VAR"):
        _required("FAKE_VAR")

# --- Defaults tests (no mocking needed, these are just constants) ---

def test_default_model():
    assert DEFAULT_MODEL == "gpt-4o-mini"

def test_router_model():
    assert ROUTER_MODEL == "gpt-4o-mini"

def test_default_max_tokens():
    assert DEFAULT_MAX_TOKENS == 4096

def test_default_temperature():
    assert DEFAULT_TEMPERATURE == 1.0

# --- Paths tests ---

# PACKAGE_ROOT should point to a real directory
def test_package_root_exists():
    assert PACKAGE_ROOT.is_dir()

# PROMPTS_DIR should exist and contain .md files
def test_prompts_dir_exists():
    assert PROMPTS_DIR.is_dir()

def test_prompts_dir_has_md_files():
    md_files = list(PROMPTS_DIR.glob("*.md"))
    assert len(md_files) == 3

# Full module reload test (integration) ---

# Importing config with all required env vars set should succeed.
def test_config_loads_with_valid_env(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "fake-openai-key")
    monkeypatch.setenv("TAVILY_API_KEY", "fake-tavily-key")

    import wedding_planner.config as config
    importlib.reload(config)

    assert config.OPENAI_API_KEY == "fake-openai-key"
    assert config.TAVILY_API_KEY == "fake-tavily-key"

# Importing config with a missing required key should crash.
def test_config_crasches_without_api_key(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.delenv("TAVILY_API_KEY", raising=False)
    monkeypatch.setattr("dotenv.load_dotenv", lambda *args, **kwargs: None)
    
    import wedding_planner.config as config

    with pytest.raises(RuntimeError):
        importlib.reload(config)