import home

from graphite_feeder.handler.event.enum import Handler as Parent


class Handler(Parent):

    KLASS = home.event.sleepiness.Event
    TITLE = "Home user sleepiness"

    def _get_url(self, name):
        url = (
            'target=alias(offset(keepLastValue({name}.{metric}), -1),"Sleepy")&'.format(
                name=name, metric=self.metric
            )
        )
        url += (
            'target=alias(offset(keepLastValue({name}.{metric}), 0),"Awake")&'.format(
                name=name, metric=self.metric
            )
        )
        url += (
            'target=alias(offset(keepLastValue({name}.{metric}), 1),"Asleep")&'.format(
                name=name, metric=self.metric
            )
        )
        return url
