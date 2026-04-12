"""Tests for the playlist search tool."""
import json

from wedding_planner.tools import search_playlists

from wedding_planner.config import CHINOOK_DB_PATH

from langchain_core.tools import BaseTool

# The @tool-decorated function must be a BaseTool.
def test_search_playlists_is_basetool():
    assert isinstance(search_playlists, BaseTool)

# Must have a name and description for the LLM to use.
def test_search_playlists_has_name_and_description():
    assert search_playlists.name
    assert search_playlists.description

# Must declare an input schema containing genre and limit
def test_search_playlists_has_expected_args():
    schema = search_playlists.args_schema
    assert schema is not None
    fields = search_playlists.args_schema.model_json_schema()
    assert "genre" in fields["properties"]
    assert "limit" in fields["properties"]

# --- Database ---

# CHINOOK_DB_PATH must point to the actual Chinook database file
def test_db_path_exists():
    assert CHINOOK_DB_PATH.exists(), f"Database not found at {CHINOOK_DB_PATH}"

# --- Return shape ---

# Every response must have the same top-level keys regardless of success or failure
def test_result_has_expected_keys():
    raw = search_playlists.invoke({"genre": "Rock", "limit": 1})
    result = json.loads(raw)
    assert "found" in result
    assert "genre" in result
    assert "tracks" in result

# The 'genre' key must echo back the input
def test_result_echoes_genre():
    raw = search_playlists.invoke({"genre": "jazz", "limit": 1})
    result = json.loads(raw)
    assert result["genre"] == "Jazz"

# Each track must have the expected fields.
def test_track_has_expected_fields():
    raw = search_playlists.invoke({"genre": "rock", "limit": 1})
    result = json.loads(raw)
    assert result["found"] is True
    track = result["tracks"][0]
    assert "artist" in track
    assert "track" in track
    assert "album" in track
    assert "duration" in track

# --- Query behavior ---

# A known genre must return found=True with tracks
def test_known_genre_returns_tracks():
    raw = search_playlists.invoke({"genre": "rock", "limit": 5})
    result = json.loads(raw)
    assert result["found"] is True
    assert len(result["tracks"]) > 0
    assert len(result["tracks"]) <= 5

# Search must be case-insensitive
def test_search_is_case_insentitive():
    raw = search_playlists.invoke({"genre": "jazz", "limit": 1})
    result = json.loads(raw)
    assert result["found"] is True

# An unknown genre must return found=False with an empty track list
def test_unknown_genre_returns_empty():
    raw = search_playlists.invoke({"genre": "Polka"})
    result = json.loads(raw)
    assert result["found"] is False
    assert result["tracks"] == []

# The limit parameter must cap the number of tracks returned
def test_limit_caps_results():
    raw = search_playlists.invoke({"genre": "Rock", "limit": 3})
    result = json.loads(raw)
    assert result["found"] is True
    assert len(result["tracks"]) <= 3