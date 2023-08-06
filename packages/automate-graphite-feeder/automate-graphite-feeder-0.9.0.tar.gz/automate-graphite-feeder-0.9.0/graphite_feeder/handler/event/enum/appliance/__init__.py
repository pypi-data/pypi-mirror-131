import home

from graphite_feeder.handler.event.enum import Handler as Parent


class Handler(Parent):

    TITLE = "Force"
    KLASS = home.event.Enum
    COLOR_LIST = "404040,666666,808080,999999,B3B3B3"

    def _get_url(self, name):
        url = 'target=alias(offset(keepLastValue({name}.{metric}), -1),"Not")&'.format(
            name=name, metric=self.metric
        )
        url += 'target=alias(offset(keepLastValue({name}.{metric}), 0),"Off")&'.format(
            name=name, metric=self.metric
        )
        url += 'target=alias(offset(keepLastValue({name}.{metric}), 1),"On")&'.format(
            name=name, metric=self.metric
        )
        return url


from graphite_feeder.handler.event.enum.appliance import light
from graphite_feeder.handler.event.enum.appliance import curtain
from graphite_feeder.handler.event.enum.appliance import socket
from graphite_feeder.handler.event.enum.appliance import sound
from graphite_feeder.handler.event.enum.appliance import thermostat
from graphite_feeder.handler.event.enum.appliance import sprinkler
