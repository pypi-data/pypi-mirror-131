import home

from graphite_feeder.handler.event.appliance.thermostat.setpoint import (
    Handler as Parent,
)


class Handler(Parent):

    KLASS = home.appliance.thermostat.presence.event.keep.setpoint.Event
    TITLE = "Setpoint maintenance(°C)"
