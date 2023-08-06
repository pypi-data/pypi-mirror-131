import home

from graphite_feeder.handler.event.appliance.float import Handler as Parent


class Handler(Parent):

    KLASS = home.appliance.light.event.temperature.Event
    TITLE = "Temperature (°)"
