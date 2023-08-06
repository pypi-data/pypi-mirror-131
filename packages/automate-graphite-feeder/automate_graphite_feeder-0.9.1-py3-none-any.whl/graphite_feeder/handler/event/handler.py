from graphite_feeder.handler.graph import Graph
from graphite_feeder.handler.event.registry import Registry


class Handler(Graph, metaclass=Registry):
    def __init__(self, home_resources, event, from_number=None, from_unit=None):
        self._home_resources = home_resources
        self._event = event
        self._from_number = from_number
        self._from_unit = from_unit
