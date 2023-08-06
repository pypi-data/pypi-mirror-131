import home

from graphite_feeder.handler.event.appliance.light.brightness import Handler as Parent


class Handler(Parent):

    KLASS = home.appliance.light.event.circadian_rhythm.brightness.Event
    TITLE = "Circadian rhythm brightness (%)"
