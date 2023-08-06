import home

from graphite_feeder.handler.event.appliance.light.hue import Handler as Parent


class Handler(Parent):

    KLASS = home.appliance.light.event.show.ending_hue.Event
    TITLE = "Show ending hue (°)"
