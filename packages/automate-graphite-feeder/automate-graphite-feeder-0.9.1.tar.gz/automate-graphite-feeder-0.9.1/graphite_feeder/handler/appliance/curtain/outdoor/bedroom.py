import home

from graphite_feeder.handler.appliance.curtain.outdoor import Handler as Parent


class Handler(Parent):

    KLASS = home.appliance.curtain.outdoor.bedroom.Appliance

    def get_datapoint(self):
        if (
            self._appliance.state.VALUE
            == home.appliance.curtain.outdoor.bedroom.state.opened.State.VALUE
        ):
            return 0
        if (
            self._appliance.state.VALUE
            == home.appliance.curtain.outdoor.bedroom.state.forced.opened.State.VALUE
        ):
            return -1
        if (
            self._appliance.state.VALUE
            == home.appliance.curtain.outdoor.bedroom.state.closed.State.VALUE
        ):
            return 1
        if (
            self._appliance.state.VALUE
            == home.appliance.curtain.outdoor.bedroom.state.forced.closed.State.VALUE
        ):
            return 2
