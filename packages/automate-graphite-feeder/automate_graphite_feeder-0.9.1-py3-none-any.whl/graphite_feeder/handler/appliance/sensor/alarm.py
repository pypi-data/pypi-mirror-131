import home

from graphite_feeder.handler.appliance import handler


class Handler(handler.Handler):

    KLASS = home.appliance.sensor.alarm.Appliance

    def _get_url(self, name):
        url = 'target=alias(offset(keepLastValue({name}.{metric}), -1),"Triggered")&'.format(
            name=name, metric=self.metric
        )
        url += (
            'target=alias(offset(keepLastValue({name}.{metric}), 0),"Armed")&'.format(
                name=name, metric=self.metric
            )
        )
        url += (
            'target=alias(offset(keepLastValue({name}.{metric}), 1),"Unarmed")&'.format(
                name=name, metric=self.metric
            )
        )
        return url

    def get_datapoint(self):
        if (
            self._appliance.state.VALUE
            == home.appliance.sensor.alarm.state.triggered.State().VALUE
        ):
            return 2
        elif (
            self._appliance.state.VALUE
            == home.appliance.sensor.alarm.state.armed.State().VALUE
        ):
            return 1
        elif (
            self._appliance.state.VALUE
            == home.appliance.sensor.alarm.state.unarmed.State().VALUE
        ):
            return 0
