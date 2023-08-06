import home

from graphite_feeder.handler.appliance.handler import Handler as Parent
from graphite_feeder.handler.event.registry import mapper


class Handler(Parent):

    KLASS = home.appliance.sensor.luxmeter.Appliance
    EVENT_KLASS = float
    TITLE = "????"

    def _get_url(self, name: str):
        return None

    @property
    def graphite_urls(self):
        urls = list()
        name = self.target_name
        for event in self._appliance.state.events:
            if event.__class__ == self.EVENT_KLASS:
                try:
                    event_handler = mapper[event.__class__]
                    event_handler = event_handler(
                        self._home_resources, event, self._from_number, self._from_unit
                    )
                    url = event_handler.get_url(name)
                    url += "&title={}".format(self.TITLE)
                    urls.append(url)
                except KeyError:
                    self._logger.warning("event {} not mapped".format(event))
                except TypeError:
                    self._logger.warning("event {} not mapped".format(event))
        return urls

    def get_datapoint(self):
        return None


from graphite_feeder.handler.appliance.sensor import (
    alarm,
    anemometer,
    luxmeter,
    motion,
    powermeter,
    rain,
    scene,
    thermometer,
)
