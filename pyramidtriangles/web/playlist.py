from __future__ import annotations
import cherrypy
from collections.abc import Mapping
from queue import Queue
from typing import Union

from ..core import PlaylistController, Settings
from ..core import RunShowCmd

# type representing the playlist state
Playlist = Mapping[str, Union[list[tuple[int, str]], int]]


@cherrypy.expose
@cherrypy.tools.json_in()
@cherrypy.tools.json_out()
class Playlist:
    def __init__(self, queue: Queue, playlist: PlaylistController):
        self.entries = Entry(playlist)
        self.queue = queue
        self.playlist = playlist

    def _current_playlist(self) -> Playlist:
        return {
            'playlist': self.playlist.current_playlist(),
            'playing': self.playlist.current_entry(),
        }

    def GET(self) -> Playlist:
        """
        Returns the current playlist of shows. [(id, show),...].
        """
        return self._current_playlist()

    def POST(self) -> Playlist:
        """
        Appends a show to the playlist and returns the new playlist.
        """
        data = cherrypy.request.json
        if 'show' not in data:
            raise cherrypy.HTTPError(400, "missing parameter 'show'")

        self.playlist.append(data['show'])
        return self._current_playlist()

    def DELETE(self) -> None:
        """
        Deletes all shows.
        """
        self.playlist.clear()

    def PUT(self) -> None:
        """
        Runs the playlist entry with {entry_id} as the current show.

        It works by setting {entry_id} to be the next playlist entry, then triggers the ShowRunner to play the next
        show.
        """
        data = cherrypy.request.json
        if 'entry_id' not in data:
            raise cherrypy.HTTPError(400, "missing parameter 'entry_id'")
        entry_id = data['entry_id']
        self.playlist.set_next(entry_id)
        self.queue.put(RunShowCmd(None))


# A playlist entry. A show can have multiple entries, each with different settings.
# All methods accessible as playlist/entries/{entry_id}
@cherrypy.expose
@cherrypy.tools.json_in()
@cherrypy.tools.json_out()
@cherrypy.popargs('entry_id')
class Entry:
    def __init__(self, playlist: PlaylistController):
        self.playlist = playlist

    def GET(self, entry_id: int) -> Settings:
        """
        Returns the settings for a playlist entry, if any.

        Setting entries have the form:
        {
          Color: { h: 1.0, s: 1.0, v: 1.0 },
          Speed: 1.5,
          ...
        }
        """
        return self.playlist.get_settings(entry_id)

    def POST(self, entry_id: int) -> Settings:
        """
        Sets the show settings for a playlist entry. Returns the new setting.

        Request data should be a JSON object mapping a setting name to a value.
        { Color: { h: 1.0, s: 1.0, v: 1.0 } }
        or
        { Speed: 1.5 }
        """
        data = cherrypy.request.json

        # Merges settings from request with settings from database, with minimal validation.
        settings = self.playlist.get_settings(entry_id)
        for (key, value) in data.items():
            if isinstance(value, (int, float, dict)):
                settings[key] = value

        self.playlist.set_settings(entry_id, settings)
        return self.playlist.get_settings(entry_id)

    def DELETE(self, entry_id: int) -> None:
        """
        Deletes a show from the playlist.
        """
        self.playlist.delete(entry_id)
