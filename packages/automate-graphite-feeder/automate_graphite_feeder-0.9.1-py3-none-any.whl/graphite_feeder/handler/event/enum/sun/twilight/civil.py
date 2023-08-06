import home

from graphite_feeder.handler.event.enum import Handler as Parent


class Handler(Parent):

    KLASS = home.event.sun.twilight.civil.Event
    TITLE = "Sun civil twilight"

    def _get_url(self, name):
        url = 'target=alias(keepLastValue({name}.{metric}),"Sunrise")&'.format(
            name=name, metric=self.metric
        )
        url += (
            'target=alias(offset(keepLastValue({name}.{metric}), 1),"Sunset")&'.format(
                name=name, metric=self.metric
            )
        )
        return url
