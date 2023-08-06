import home

from graphite_feeder.handler.event.enum import Handler as Parent


class Handler(Parent):

    KLASS = home.event.waveform.Event
    TITLE = "Waveform"

    def _get_url(self, name):
        url = 'target=alias(offset(keepLastValue({name}.{metric}), 1),"Saw")&'.format(
            name=name, metric=self.metric
        )
        url += 'target=alias(offset(keepLastValue({name}.{metric}), 0),"Sine")&'.format(
            name=name, metric=self.metric
        )
        url += 'target=alias(offset(keepLastValue({name}.{metric}), -1),"HalfSine")&'.format(
            name=name, metric=self.metric
        )
        url += 'target=alias(offset(keepLastValue({name}.{metric}), -2),"Triangle")&'.format(
            name=name, metric=self.metric
        )
        url += (
            'target=alias(offset(keepLastValue({name}.{metric}), -3),"Pulse")&'.format(
                name=name, metric=self.metric
            )
        )
        return url
