import home

from graphite_feeder.handler.appliance.light import Handler as Parent


class Handler(Parent):

    KLASS = home.appliance.light.indoor.dimmerable.Appliance

    def _get_url(self, name):
        url = 'target=alias(offset(keepLastValue({name}.{metric}), -4),"Show")&'.format(
            name=name, metric=self.metric
        )
        url += 'target=alias(offset(keepLastValue({name}.{metric}), -3),"Circadian rhythm")&'.format(
            name=name, metric=self.metric
        )
        url += 'target=alias(offset(keepLastValue({name}.{metric}), -2),"Lux balancing")&'.format(
            name=name, metric=self.metric
        )
        url += 'target=alias(offset(keepLastValue({name}.{metric}), -1),"Forced on")&'.format(
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
            == home.appliance.light.indoor.dimmerable.state.off.State().VALUE
        ):
            return 0
        if (
            self._appliance.state.VALUE
            == home.appliance.light.indoor.dimmerable.state.on.State().VALUE
        ):
            return 1
        if (
            self._appliance.state.VALUE
            == home.appliance.light.indoor.dimmerable.state.forced.on.State().VALUE
        ):
            return 2
        if (
            self._appliance.state.VALUE
            == home.appliance.light.indoor.dimmerable.state.forced.lux_balance.State().VALUE
        ):
            return 3
        if (
            self._appliance.state.VALUE
            == home.appliance.light.indoor.dimmerable.state.forced.circadian_rhythm.State().VALUE
        ):
            return 4
        if (
            self._appliance.state.VALUE
            == home.appliance.light.indoor.dimmerable.state.forced.show.State().VALUE
        ):
            return 5
