import home

from graphite_feeder.handler.appliance import handler


class Handler(handler.Handler):

    KLASS = home.appliance.sprinkler.Appliance

    def _get_url(self, name):
        url = 'target=alias(offset(keepLastValue({name}.{metric}), -4),"Forced Off")&'.format(
            name=name, metric=self.metric
        )
        url += 'target=alias(offset(keepLastValue({name}.{metric}), -3),"Forced Partially On")&'.format(
            name=name, metric=self.metric
        )
        url += 'target=alias(offset(keepLastValue({name}.{metric}), -2),"Forced On")&'.format(
            name=name, metric=self.metric
        )
        url += 'target=alias(offset(keepLastValue({name}.{metric}), -1),"Partially On")&'.format(
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
            == home.appliance.sprinkler.state.off.State().VALUE
        ):
            return 0
        if (
            self._appliance.state.VALUE
            == home.appliance.sprinkler.state.on.State().VALUE
        ):
            return 1
        if (
            self._appliance.state.VALUE
            == home.appliance.sprinkler.state.partially_on.State().VALUE
        ):
            return 2
        if (
            self._appliance.state.VALUE
            == home.appliance.sprinkler.state.forced.on.State().VALUE
        ):
            return 3
        if (
            self._appliance.state.VALUE
            == home.appliance.sprinkler.state.forced.partially_on.State().VALUE
        ):
            return 4
        if (
            self._appliance.state.VALUE
            == home.appliance.sprinkler.state.forced.off.State().VALUE
        ):
            return 5
