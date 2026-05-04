#!/usr/bin/env python3
"""FTS5 memory search — full-text search across brand profiles for cross-session recall."""

import argparse
import json
import os
import sqlite3
import sys


def _ensure_table(conn: sqlite3.Connection) -> None:
    conn.execute(
        "CREATE VIRTUAL TABLE IF NOT EXISTS brand_memory USING fts5("
        "name, industry, personality, voice_tone, tagline, raw_json"
        ")"
    )


def _index_profile(conn: sqlite3.Connection, profile_path: str) -> None:
    _ensure_table(conn)

    with open(profile_path) as f:
        data = json.load(f)

    name = data.get("name", "")
    industry = data.get("industry", "")
    personality = ", ".join(data.get("personality_words", []))
    voice_tone = data.get("voice_tone", "")
    tagline = data.get("tagline", "")
    raw_json = json.dumps(data)

    conn.execute(
        "INSERT INTO brand_memory (name, industry, personality, voice_tone, tagline, raw_json) "
        "VALUES (?, ?, ?, ?, ?, ?)",
        (name, industry, personality, voice_tone, tagline, raw_json),
    )
    conn.commit()


def _search_profiles(conn: sqlite3.Connection, query: str) -> list[dict]:
    _ensure_table(conn)

    cursor = conn.execute(
        "SELECT name, industry, personality, voice_tone, tagline, raw_json, rank "
        "FROM brand_memory WHERE brand_memory MATCH ? "
        "ORDER BY rank",
        (query,),
    )
    results: list[dict] = []
    for row in cursor.fetchall():
        name, industry, personality, voice_tone, tagline, raw_json_str, rank = row
        results.append(
            {
                "name": name,
                "industry": industry,
                "personality": personality,
                "voice_tone": voice_tone,
                "tagline": tagline,
                "rank": rank,
                "profile": json.loads(raw_json_str),
            }
        )
    return results


def main() -> None:
    parser = argparse.ArgumentParser(
        description="FTS5 memory search — cross-session brand recall"
    )
    parser.add_argument(
        "--db",
        default=os.path.expanduser("~/.hermes/forge_memory.db"),
        help="SQLite database path",
    )
    parser.add_argument(
        "--index", default=None, help="Path to brand_profile.json to index"
    )
    parser.add_argument("--search", default=None, help="FTS5 search query")
    args = parser.parse_args()

    if not args.index and not args.search:
        print("ERROR: --index or --search required", file=sys.stderr)
        parser.print_help()
        sys.exit(1)

    db_dir = os.path.dirname(os.path.abspath(os.path.expanduser(args.db)))
    os.makedirs(db_dir, exist_ok=True)

    conn = sqlite3.connect(os.path.expanduser(args.db))

    try:
        if args.index:
            _index_profile(conn, args.index)
            print(f"[+] Indexed: {args.index}")

        if args.search:
            results = _search_profiles(conn, args.search)
            print(json.dumps(results, indent=2))
    finally:
        conn.close()


if __name__ == "__main__":
    main()
