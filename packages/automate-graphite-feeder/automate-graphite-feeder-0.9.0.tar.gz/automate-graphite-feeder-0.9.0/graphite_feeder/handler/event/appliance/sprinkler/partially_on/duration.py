import home

from graphite_feeder.handler.event.appliance.int import Handler as Parent


class Handler(Parent):

    KLASS = home.appliance.sprinkler.event.partially_on.duration.Event
    TITLE = "Sprinkling time duration reduced (seconds)"
