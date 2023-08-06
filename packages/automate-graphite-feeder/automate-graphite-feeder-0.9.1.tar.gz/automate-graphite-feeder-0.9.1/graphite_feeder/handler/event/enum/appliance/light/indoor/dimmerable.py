import home

from graphite_feeder.handler.event.enum.appliance import Handler as Parent


class Handler(Parent):

    KLASS = home.appliance.light.indoor.dimmerable.event.forced.event.Event

    def _get_url(self, name):
        url = 'target=alias(offset(keepLastValue({name}.{metric}), -4),"Not")&'.format(
            name=name, metric=self.metric
        )
        url += (
            'target=alias(offset(keepLastValue({name}.{metric}), -3),"Show")&'.format(
                name=name, metric=self.metric
            )
        )
        url += 'target=alias(offset(keepLastValue({name}.{metric}), -2),"LuxBalance")&'.format(
            name=name, metric=self.metric
        )
        url += 'target=alias(offset(keepLastValue({name}.{metric}), -1),"CircadianRhythm")&'.format(
            name=name, metric=self.metric
        )
        url += 'target=alias(offset(keepLastValue({name}.{metric}), 0),"Off")&'.format(
            name=name, metric=self.metric
        )
        url += 'target=alias(offset(keepLastValue({name}.{metric}), 1),"On")&'.format(
            name=name, metric=self.metric
        )
        return url
