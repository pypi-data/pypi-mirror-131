import home

from graphite_feeder.handler.event.enum import Handler as Parent


class Handler(Parent):

    KLASS = home.event.user.Event
    TITLE = "User"
    A = "A"
    B = "B"
    C = "C"

    def _get_url(self, name):
        url = 'target=alias(offset(keepLastValue({name}.{metric}), -1),"{label}")&'.format(
            name=name, metric=self.metric, label=self.C
        )
        url += (
            'target=alias(offset(keepLastValue({name}.{metric}), 0),"{label}")&'.format(
                name=name, metric=self.metric, label=self.B
            )
        )
        url += (
            'target=alias(offset(keepLastValue({name}.{metric}), 1),"{label}")&'.format(
                name=name, metric=self.metric, label=self.A
            )
        )
        return url
