"""
SQLite Cache module.

This module provides the following classes:

- SqliteCache
"""
import json
import sqlite3
from typing import Any, Optional


class SqliteCache:
    """
    The SqliteCache object to cache search results from Marvel.

    Parameters
    ----------
    db_name: str
        Path and database name to use.

    Returns
    -------
    SqliteCache
        A :class:`SqliteCache` Object.
    """

    def __init__(self, db_name: str = "esak_cache.db") -> None:
        """Intialize a new SqliteCache."""
        self.con = sqlite3.connect(db_name)
        self.cur = self.con.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS responses (key, json)")

    def get(self, key: str) -> Optional[Any]:
        """
        Retrieve data from the cache database.

        Parameters
        ----------
        key: str
            value to search for.
        """
        self.cur.execute("SELECT json FROM responses WHERE key = ?", (key,))
        result = self.cur.fetchone()

        if result:
            return json.loads(result[0])

        return None

    def store(self, key: str, value: str) -> None:
        """
        Save data to the cache database.

        Parameters
        ----------
        key: str
            Item id.
        value: str
            data to save.
        """
        self.cur.execute(
            "INSERT INTO responses(key, json) VALUES(?, ?)", (key, json.dumps(value))
        )
        self.con.commit()
