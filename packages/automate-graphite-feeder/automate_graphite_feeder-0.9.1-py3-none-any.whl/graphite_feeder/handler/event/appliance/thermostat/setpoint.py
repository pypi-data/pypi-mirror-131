import home

from graphite_feeder.handler.event.appliance.float import Handler as Parent


class Handler(Parent):

    KLASS = home.appliance.thermostat.presence.event.setpoint.Event
    TITLE = "Setpoint (°C)"
