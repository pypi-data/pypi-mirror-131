import home

from graphite_feeder.handler.appliance.socket.energy_guard import Handler as Parent


class Handler(Parent):

    KLASS = home.appliance.socket.presence.christmas.Appliance

    def get_datapoint(self):
        if (
            self._appliance.state.VALUE
            == home.appliance.socket.presence.christmas.state.on.State().VALUE
        ):
            return 1
        if (
            self._appliance.state.VALUE
            == home.appliance.socket.presence.christmas.state.forced.on.State().VALUE
        ):
            return 2
        if (
            self._appliance.state.VALUE
            == home.appliance.socket.presence.christmas.state.off.State().VALUE
        ):
            return 0
        if (
            self._appliance.state.VALUE
            == home.appliance.socket.presence.christmas.state.forced.off.State().VALUE
        ):
            return -1
