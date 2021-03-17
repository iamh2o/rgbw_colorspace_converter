from collections import defaultdict
from queue import Queue
import cherrypy

from ..color import HSV
from ..core import ShowKnobCmd
from ..grid import Pyramid
from ..model.null import NullModel
from ..shows import load_shows


@cherrypy.expose
@cherrypy.tools.json_in()
@cherrypy.tools.json_out()
class ShowKnob:
    def __init__(self, queue: Queue):
        self.queue = queue
        self.knobs = defaultdict(list)

        null_pyramid = Pyramid.build_single(NullModel())
        for (name, cls) in load_shows():
            show = cls(null_pyramid)
            if show.knobs:
                self.knobs[name] = show.knobs.json_array

    @cherrypy.popargs('show')
    def GET(self, show):
        """
        Returns the available knobs for the given show.

        [{
            name: 'Main Color',
            value: {
              default: { h: 1.0, s: 1.0, v: 1.0},
            },
            type: 'HSVKnob'
        }, {
            name: 'Speed',
            value: {
              default: 1.0,
            },
            type: 'ValueKnob'
        },
        .
        .
        .
        ]
        """
        return self.knobs[show]

    def POST(self) -> None:
        """
        Sets the knob `name` to value `value` for show `show`
        """
        data = cherrypy.request.json
        for p in ['show', 'name', 'value']:
            if p not in data.keys():
                raise cherrypy.HTTPError(400, f"missing parameter '{p}'")

        value = data['value']

        if isinstance(value, dict):
            if any([c not in value.keys() for c in 'hsv']):
                raise cherrypy.HTTPError(400, 'missing HSV parameter')

            try:
                value = HSV(*[value[c] for c in 'hsv'])
            except TypeError as e:
                raise cherrypy.HTTPError(400, e)

        self.queue.put_nowait(ShowKnobCmd(show=data['show'], name=data['name'], value=value))
