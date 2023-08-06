import home

from graphite_feeder.handler.appliance import handler


class Handler(handler.Handler):

    KLASS = home.appliance.curtain.outdoor.Appliance
    TITLE = "State"

    def _get_url(self, name):
        url = 'target=alias(offset(keepLastValue({name}.{metric}), -1),"Forced closed")&'.format(
            name=name, metric=self.metric
        )
        url += (
            'target=alias(offset(keepLastValue({name}.{metric}), 0),"Closed")&'.format(
                name=name, metric=self.metric
            )
        )
        url += (
            'target=alias(offset(keepLastValue({name}.{metric}), 1),"Opened")&'.format(
                name=name, metric=self.metric
            )
        )
        url += 'target=alias(offset(keepLastValue({name}.{metric}), 2),"Forced Opened")&'.format(
            name=name, metric=self.metric
        )
        return url

    def get_datapoint(self):
        if (
            self._appliance.state.VALUE
            == home.appliance.curtain.outdoor.state.opened.State.VALUE
        ):
            return 0
        if (
            self._appliance.state.VALUE
            == home.appliance.curtain.outdoor.state.forced.opened.State.VALUE
        ):
            return -1
        if (
            self._appliance.state.VALUE
            == home.appliance.curtain.outdoor.state.closed.State.VALUE
        ):
            return 1
        if (
            self._appliance.state.VALUE
            == home.appliance.curtain.outdoor.state.forced.closed.State.VALUE
        ):
            return 2


from graphite_feeder.handler.appliance.curtain.outdoor import bedroom
