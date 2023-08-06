import home

from graphite_feeder.handler.event.enum import Handler as Parent


class Handler(Parent):

    KLASS = home.event.sun.hit.Event
    TITLE = "Sun position"

    def _get_url(self, name):
        url = 'target=alias(keepLastValue({name}.{metric}),"Is gone")&'.format(
            name=name, metric=self.metric
        )
        url += (
            'target=alias(offset(keepLastValue({name}.{metric}), 1),"Is over")&'.format(
                name=name, metric=self.metric
            )
        )
        return url
