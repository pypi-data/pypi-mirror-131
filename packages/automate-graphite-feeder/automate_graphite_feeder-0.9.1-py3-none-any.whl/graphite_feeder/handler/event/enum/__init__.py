from abc import abstractmethod
import home

from graphite_feeder.handler.event import handler


class Handler(handler.Handler):

    KLASS = home.event.Enum

    @property
    def metric(self):
        return self.module

    def _get_url(self, name):
        url = 'target=alias(offset(keepLastValue({name}.{metric}), 0),"Off")&'.format(
            name=name, metric=self.metric
        )
        url += 'target=alias(offset(keepLastValue({name}.{metric}), 1),"On")&'.format(
            name=name, metric=self.metric
        )
        return url

    def get_datapoint(self):
        values = {v: e for e, v in enumerate(self.KLASS)}
        return values[self._event]


from graphite_feeder.handler.event.enum import (
    appliance,
    holiday,
    alarm,
    clima,
    power,
    sun,
    courtesy,
    enable,
    motion,
    presence,
    rain,
    show,
    sleepiness,
    temperature,
    wind,
    scene,
    user,
    elapsed,
    toggle,
)
