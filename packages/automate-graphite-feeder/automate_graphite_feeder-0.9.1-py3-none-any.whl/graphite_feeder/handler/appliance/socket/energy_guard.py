import home

from graphite_feeder.handler.appliance import handler


class Handler(handler.Handler):

    KLASS = home.appliance.socket.energy_guard.Appliance

    def _get_url(self, name):
        url = 'target=alias(offset(keepLastValue({name}.{metric}), -1),"Forced on")&'.format(
            name=name, metric=self.metric
        )
        url += 'target=alias(offset(keepLastValue({name}.{metric}), 0),"On")&'.format(
            name=name, metric=self.metric
        )
        url += 'target=alias(offset(keepLastValue({name}.{metric}), 1),"Off")&'.format(
            name=name, metric=self.metric
        )
        url += 'target=alias(offset(keepLastValue({name}.{metric}), 2),"Forced off")&'.format(
            name=name, metric=self.metric
        )
        return url

    def get_datapoint(self):
        if (
            self._appliance.state.VALUE
            == home.appliance.socket.energy_guard.state.on.State().VALUE
        ):
            return 1
        if (
            self._appliance.state.VALUE
            == home.appliance.socket.energy_guard.state.forced.on.State().VALUE
        ):
            return 2
        if (
            self._appliance.state.VALUE
            == home.appliance.socket.energy_guard.state.off.State().VALUE
        ):
            return 0
        if (
            self._appliance.state.VALUE
            == home.appliance.socket.energy_guard.state.forced.off.State().VALUE
        ):
            return -1
