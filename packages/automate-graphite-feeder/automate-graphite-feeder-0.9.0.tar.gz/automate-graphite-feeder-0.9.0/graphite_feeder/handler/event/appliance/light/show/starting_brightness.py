import home

from graphite_feeder.handler.event.appliance.light.brightness import Handler as Parent


class Handler(Parent):

    KLASS = home.appliance.light.event.show.starting_brightness.Event
    TITLE = "Show starting brightness (%)"
