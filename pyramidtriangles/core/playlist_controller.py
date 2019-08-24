from __future__ import annotations
import json
import sqlite3
from contextlib import closing
from typing import Optional, Union

HSVValues = dict[str, float]
# setting_value can be int, float, or an HSV triple
Value = Union[int, float, HSVValues]
# setting_name -> setting_value
Settings = dict[str, Value]

# At least one connection must be retained to the in-memory database or it will be cleared.
_db_conn_keep_open: sqlite3.Connection


class PlaylistController:
    """
    Controller to handle in-memory database lookups for playlists.

    This class and methods are thread-safe. At least one connection must be kept open for the DB to stay in memory.
    """

    @staticmethod
    def _connect() -> sqlite3.Connection:
        return sqlite3.connect('file::memory:?cache=shared', timeout=0.5, uri=True)

    @classmethod
    def setup_database(cls):
        """Needs to be called once to set up the database."""
        global _db_conn_keep_open
        _db_conn_keep_open = cls._connect()
        with _db_conn_keep_open as conn:
            # Pragmas to increase performance from defaults
            conn.execute("PRAGMA journal_mode = 'WAL'")
            conn.execute('PRAGMA temp_store = 2')
            conn.execute('PRAGMA synchronous = OFF')  # Use NORMAL if persisting DB
            conn.execute('PRAGMA cache_size = -64000')
            conn.execute('CREATE TABLE IF NOT EXISTS Playlist (show TEXT NOT NULL, settings TEXT)')
            conn.execute('CREATE TABLE IF NOT EXISTS Current (playing INTEGER, FOREIGN KEY (playing) REFERENCES Playlist(ROWID))')
            conn.execute('INSERT INTO Current VALUES (NULL)')

    def current_playlist(self) -> list[tuple[int, str]]:
        """
        Returns the current playlist of shows. [(id, show),...].
        Uses a list instead of dict to retain ordering.
        """
        with closing(self._connect()) as conn:
            cursor = conn.execute('SELECT rowid, show FROM Playlist ORDER BY rowid')
            return cursor.fetchall()

    def current_entry(self) -> Optional[int]:
        """
        Returns the entry_id of the playing show, or None.
        """
        with closing(self._connect()) as conn:
            cursor = conn.execute('SELECT playing FROM Current LIMIT 1')
            return cursor.fetchone()[0]

    def next(self) -> Optional[str]:
        """
        Gets the next show from the playlist.

        Uses the 'Current' table to determine the next show on the playlist, and advances the Current show.
        If the Current show is NULL, selects the first item in the playlist.
        If the playlist is empty, returns None.
        """
        with closing(self._connect()) as conn:  # context manager on the connection
            # Get next show from database.
            cursor = conn.execute('''SELECT rowid, show FROM Playlist WHERE rowid >
                IFNULL((SELECT playing FROM Current LIMIT 1),-1)
                LIMIT 1''')
            next_show = cursor.fetchone()

            # Handle looping to the first show if we've reached the end of the playlist.
            if next_show is None:
                cursor.execute('SELECT rowid, show FROM Playlist ORDER BY rowid LIMIT 1')
                next_show = cursor.fetchone()

            # next_show could still be None if Playlist is also empty
            if next_show is None:
                return None

            (entry_id, show) = next_show
            with conn:
                cursor.execute('UPDATE Current SET playing = (?)', (entry_id,))
            return show

    def set_next(self, entry_id: int) -> None:
        """
        Sets the next show in the playlist to be {entry_id}.
        """
        with closing(self._connect()) as conn:
            # Get previous show from database.
            cursor = conn.execute('SELECT MAX(rowid) FROM Playlist WHERE rowid < (?) LIMIT 1', (entry_id,))
            prev_id = cursor.fetchone()[0]
            with conn:
                cursor.execute('UPDATE Current SET playing = (?)', (prev_id,))

    def append(self, show: str) -> int:
        """
        Appends a show to the playlist and returns the new entry_id.
        """
        with closing(self._connect()) as conn:
            with conn:
                cursor = conn.execute('INSERT INTO Playlist VALUES (?, NULL)', (show,))
                return cursor.lastrowid

    def delete(self, entry_id: int) -> None:
        """
        Deletes a show from the playlist.
        """
        with closing(self._connect()) as conn:
            with conn:
                conn.execute('DELETE FROM Playlist WHERE rowid = (?)', (entry_id,))

    def clear(self) -> None:
        """
        Clears the whole playlist.
        """
        with closing(self._connect()) as conn:
            with conn:
                cursor = conn.execute('DELETE FROM Playlist')
                cursor.execute('UPDATE Current SET playing = NULL')

    def get_settings(self, entry_id: int) -> Settings:
        """
        Returns the settings for a playlist entry, if any.
        """
        with closing(self._connect()) as conn:
            cursor = conn.execute('SELECT settings FROM Playlist WHERE rowid = (?)', (entry_id,))
            data = cursor.fetchone()[0]
            return {} if data is None else json.loads(data)

    def set_settings(self, entry_id: int, settings: Settings) -> None:
        """
        Sets settings for a playlist entry.
        """
        data = json.dumps(settings)
        with closing(self._connect()) as conn:
            with conn:
                conn.execute('UPDATE Playlist SET settings = (?) WHERE rowid = (?)', (data, entry_id))
