import home

from graphite_feeder.handler.appliance import handler


class Handler(handler.Handler):

    KLASS = home.appliance.sensor.rainmeter.Appliance

    def _get_url(self, name):
        url = (
            'target=alias(offset(keepLastValue({name}.{metric}), 0),"Raining")&'.format(
                name=name, metric=self.metric
            )
        )
        url += (
            'target=alias(offset(keepLastValue({name}.{metric}), 1),"No rain")&'.format(
                name=name, metric=self.metric
            )
        )
        return url

    def get_datapoint(self):
        if (
            self._appliance.state.VALUE
            == home.appliance.sensor.rainmeter.state.gentle.State().VALUE
        ):
            return 1
        if (
            self._appliance.state.VALUE
            == home.appliance.sensor.rainmeter.state.no.State().VALUE
        ):
            return 0
