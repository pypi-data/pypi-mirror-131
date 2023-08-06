import home

from graphite_feeder.handler.appliance.light.indoor.dimmerable import Handler as Parent


class Handler(Parent):

    KLASS = home.appliance.light.indoor.hue.Appliance

    def get_datapoint(self):
        if (
            self._appliance.state.VALUE
            == home.appliance.light.indoor.hue.state.off.State().VALUE
        ):
            return 0
        if (
            self._appliance.state.VALUE
            == home.appliance.light.indoor.hue.state.on.State().VALUE
        ):
            return 1
        if (
            self._appliance.state.VALUE
            == home.appliance.light.indoor.hue.state.forced.on.State().VALUE
        ):
            return 2
        if (
            self._appliance.state.VALUE
            == home.appliance.light.indoor.hue.state.forced.lux_balance.State().VALUE
        ):
            return 3
        if (
            self._appliance.state.VALUE
            == home.appliance.light.indoor.hue.state.forced.circadian_rhythm.State().VALUE
        ):
            return 4
        if (
            self._appliance.state.VALUE
            == home.appliance.light.indoor.hue.state.forced.show.State().VALUE
        ):
            return 5
