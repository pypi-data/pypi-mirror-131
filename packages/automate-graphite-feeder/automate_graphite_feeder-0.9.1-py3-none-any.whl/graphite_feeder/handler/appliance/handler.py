import logging

from graphite_feeder.handler.graph import Graph
from graphite_feeder.handler.appliance.registry import Registry
from graphite_feeder.handler.event.registry import mapper


class Handler(Graph, metaclass=Registry):

    COLOR_LIST = "{},{},{},{},{},{},{}".format(
        Graph.GREEN,
        Graph.YELLOW,
        Graph.ORANGE,
        Graph.RED,
        Graph.VIOLET,
        Graph.MAGENTA,
        Graph.CYAN,
    )
    TITLE = "State"

    def __init__(self, home_resources, appliance, from_number=None, from_unit=None):
        self._home_resources = home_resources
        self._appliance = appliance
        self._num_of_events = len(appliance.state.events) + 1  # plus the appliance state itself
        self._logger = logging.getLogger(__name__)
        self._from_number = from_number
        self._from_unit = from_unit
        self._urls = self.graphite_urls
        self._i = 0

    @property
    def target_name(self):
        return self._appliance.name.replace(" ", "_")

    def __iter__(self):
        return self

    def __next__(self):
        if self._i < self._num_of_events:
            try:
                url = self._urls[self._i]
            except IndexError:
                raise StopIteration()
            self._i += 1
            return url
        else:
            raise StopIteration()

    @property
    def graphite_urls(self):
        urls = list()
        name = self.target_name
        if self.get_datapoint() is not None:
            url = self.get_url(name)
            urls.append(url)
        for event in self._appliance.state.events:
            try:
                event_handler = mapper[event.__class__]
                event_handler = event_handler(
                    self._home_resources, event, self._from_number, self._from_unit
                )
                url = event_handler.get_url(name)
                if url:
                    urls.append(url)
            except KeyError:
                self._logger.warning("event {} not mapped".format(event))
            except TypeError:
                self._logger.warning("event {} not mapped".format(event))
        return urls
