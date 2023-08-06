import home

from graphite_feeder.handler.event.appliance.light.hue import Handler as Parent


class Handler(Parent):

    KLASS = home.appliance.light.event.show.starting_hue.Event
    TITLE = "Show starting hue (°)"
