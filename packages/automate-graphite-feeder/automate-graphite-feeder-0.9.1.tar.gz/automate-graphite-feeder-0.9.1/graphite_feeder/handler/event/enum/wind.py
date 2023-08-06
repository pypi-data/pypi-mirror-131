import home

from graphite_feeder.handler.event.enum import Handler as Parent


class Handler(Parent):

    KLASS = home.event.wind.Event
    TITLE = "Wind"
    STRONG = "strong"
    WEAK = "weak"

    def _get_url(self, name):
        url = 'target=alias(keepLastValue({name}.{metric}),"{label}")&'.format(
            name=name, metric=self.metric, label=self.WEAK
        )
        url += (
            'target=alias(offset(keepLastValue({name}.{metric}), 1),"{label}")&'.format(
                name=name, metric=self.metric, label=self.STRONG
            )
        )
        return url
