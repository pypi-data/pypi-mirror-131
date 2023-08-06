import home

from graphite_feeder.handler.event.enum import Handler as Parent


class Handler(Parent):

    KLASS = home.event.holiday.christmas.Event
    TITLE = "Christmas"

    def _get_url(self, name):
        url = 'target=alias(offset(keepLastValue({name}.{metric}), -2),"Over")&'.format(
            name=name, metric=self.metric
        )
        url += (
            'target=alias(offset(keepLastValue({name}.{metric}), -1),"Time")&'.format(
                name=name, metric=self.metric
            )
        )
        url += 'target=alias(offset(keepLastValue({name}.{metric}), 0),"Eve")&'.format(
            name=name, metric=self.metric
        )
        url += 'target=alias(offset(keepLastValue({name}.{metric}), 1),"Day")&'.format(
            name=name, metric=self.metric
        )
        return url
