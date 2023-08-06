import home

from graphite_feeder.handler.event.enum import Handler as Parent


class Handler(Parent):

    KLASS = home.event.motion.Event
    TITLE = "Motion"

    def _get_url(self, name):
        url = 'target=alias(keepLastValue({name}.{metric}),"Missed")&'.format(
            name=name, metric=self.metric
        )
        url += (
            'target=alias(offset(keepLastValue({name}.{metric}), 1),"Spotted")&'.format(
                name=name, metric=self.metric
            )
        )
        return url
