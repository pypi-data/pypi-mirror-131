import home

from graphite_feeder.handler.appliance.light import Handler as Parent


class Handler(Parent):

    KLASS = home.appliance.light.zone.Appliance

    def _get_url(self, name):
        url = 'target=alias(offset(keepLastValue({name}.{metric}), -4),"Forced Off")&'.format(
            name=name, metric=self.metric
        )
        url += 'target=alias(offset(keepLastValue({name}.{metric}), -3),"Forced On")&'.format(
            name=name, metric=self.metric
        )
        url += 'target=alias(offset(keepLastValue({name}.{metric}), -2),"Alarmed Off")&'.format(
            name=name, metric=self.metric
        )
        url += 'target=alias(offset(keepLastValue({name}.{metric}), -1),"Alarmed On")&'.format(
            name=name, metric=self.metric
        )
        url += 'target=alias(offset(keepLastValue({name}.{metric}), 0),"On")&'.format(
            name=name, metric=self.metric
        )
        url += 'target=alias(offset(keepLastValue({name}.{metric}), 1),"Off")&'.format(
            name=name, metric=self.metric
        )
        return url

    def get_datapoint(self):
        if (
            self._appliance.state.VALUE
            == home.appliance.light.zone.state.off.State().VALUE
        ):
            return 0
        if (
            self._appliance.state.VALUE
            == home.appliance.light.zone.state.on.State().VALUE
        ):
            return 1
        if (
            self._appliance.state.VALUE
            == home.appliance.light.zone.state.alarmed.on.State().VALUE
        ):
            return 2
        if (
            self._appliance.state.VALUE
            == home.appliance.light.zone.state.alarmed.off.State().VALUE
        ):
            return 3
        if (
            self._appliance.state.VALUE
            == home.appliance.light.zone.state.forced.on.State().VALUE
        ):
            return 4
        if (
            self._appliance.state.VALUE
            == home.appliance.light.zone.state.forced.off.State().VALUE
        ):
            return 5
