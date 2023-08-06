import home

from graphite_feeder.handler.event.appliance.light.brightness import Handler as Parent


class Handler(Parent):

    KLASS = home.appliance.light.event.show.ending_brightness.Event
    TITLE = "Show ending brightness (%)"
