import home

from graphite_feeder.handler.event.enum import Handler as Parent


class Handler(Parent):

    KLASS = home.event.sun.brightness.Event
    TITLE = "Sun brightness"

    def _get_url(self, name):
        url = 'target=alias(offset(keepLastValue({name}.{metric}), -1),"DeepDark")&'.format(
            name=name, metric=self.metric
        )
        url += 'target=alias(keepLastValue({name}.{metric}),"Dark")&'.format(
            name=name, metric=self.metric
        )
        url += (
            'target=alias(offset(keepLastValue({name}.{metric}), 1),"Bright")&'.format(
                name=name, metric=self.metric
            )
        )
        return url
