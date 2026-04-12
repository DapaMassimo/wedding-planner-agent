"""
Playlist search tool backed by the Chinook SQLite database.

Queries the local music database for tracks matching a genre.
Used by the DJ agent to find wedding-appropriate music.
"""
import sqlite3

from typing import Any

import json

from langchain_core.tools import tool

from wedding_planner.config import CHINOOK_DB_PATH


def _get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(str(CHINOOK_DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn

@tool
def search_playlists(genre: str, limit: int = 20) -> str:
    """Search the music database for tracks matching a genre.

    Use this tool when you need to find songs for a wedding playlist.
    Pass the genre name (e.g. "Rock", "Jazz", "Latin", "Pop", "R&B/Soul",
    "Classical", "Blues", "Raggae", "Bossa Nova", "Hip Hop/Rap",
    "Electronica/Dance", "Easy Listening", "World").

    Returns a formatted list of tracks with artist, album and duration.
    """
    conn = _get_connection()
    try:
        rows = conn.execute(
            """
            SELECT
                t.Name AS track,
                a.Name AS artist,
                al.Title AS album,
                g.Name AS genre,
                t.Milliseconds AS ms
            FROM Track t
            JOIN Genre  g  ON t.GenreId  = g.GenreId
            JOIN Album  al ON t.AlbumId  = al.AlbumId
            JOIN Artist a  ON al.ArtistId = a.ArtistId
            WHERE LOWER(g.Name) LIKE '%' || LOWER(?) || '%'
            ORDER BY a.Name, al.Title, t.Name
            LIMIT ?
            """,
            (genre, limit),
        ).fetchall()
    finally:
        conn.close()

    tracks = [
        {
            "artist": r["artist"],
            "track": r["track"],
            "album": r["album"],
            "genre": r["genre"],
            "duration": f"{r['ms'] // 60000}:{(r['ms'] % 60000) // 1000:02d}"
        }
        for r in rows
    ]

    result = {
        "found": len(tracks) > 0,
        "genre": tracks[0]["genre"] if tracks else genre,
        "tracks": tracks
    }
    return json.dumps(result)