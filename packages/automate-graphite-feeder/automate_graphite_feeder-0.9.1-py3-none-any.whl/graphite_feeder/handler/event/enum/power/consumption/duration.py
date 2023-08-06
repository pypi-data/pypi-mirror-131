import home

from graphite_feeder.handler.event.enum import Handler as Parent


class Handler(Parent):

    KLASS = home.event.power.consumption.duration.Event
    TITLE = "Power consumption duration"

    def _get_url(self, name):
        url = 'target=alias(keepLastValue({name}.{metric}),"Long")&'.format(
            name=name, metric=self.metric
        )
        url += (
            'target=alias(offset(keepLastValue({name}.{metric}), 1),"Short")&'.format(
                name=name, metric=self.metric
            )
        )
        return url
