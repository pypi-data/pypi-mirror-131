import home

from graphite_feeder.handler.appliance.curtain.outdoor import Handler as Parent


class Handler(Parent):

    KLASS = home.appliance.curtain.indoor.blackout.Appliance

    def get_datapoint(self):
        if (
            self._appliance.state.VALUE
            == home.appliance.curtain.indoor.blackout.state.opened.State.VALUE
        ):
            return 0
        if (
            self._appliance.state.VALUE
            == home.appliance.curtain.indoor.blackout.state.forced.opened.State.VALUE
        ):
            return -1
        if (
            self._appliance.state.VALUE
            == home.appliance.curtain.indoor.blackout.state.closed.State.VALUE
        ):
            return 1
        if (
            self._appliance.state.VALUE
            == home.appliance.curtain.indoor.blackout.state.forced.closed.State.VALUE
        ):
            return 2
