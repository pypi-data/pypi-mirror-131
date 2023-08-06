import home

from graphite_feeder.handler.event.enum import Handler as Parent


class Handler(Parent):

    KLASS = home.event.clima.season.Event
    TITLE = "Clima season"

    def _get_url(self, name):
        url = 'target=alias(offset(keepLastValue({name}.{metric}), -2),"Fall")&'.format(
            name=name, metric=self.metric
        )
        url += (
            'target=alias(offset(keepLastValue({name}.{metric}), -1),"Summer")&'.format(
                name=name, metric=self.metric
            )
        )
        url += (
            'target=alias(offset(keepLastValue({name}.{metric}), 0),"Spring")&'.format(
                name=name, metric=self.metric
            )
        )
        url += (
            'target=alias(offset(keepLastValue({name}.{metric}), 1),"Winter")&'.format(
                name=name, metric=self.metric
            )
        )
        return url
