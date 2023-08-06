import home

from graphite_feeder.handler.event.appliance.int import Handler as Parent


class Handler(Parent):

    KLASS = home.appliance.light.event.show.cycles.Event
    TITLE = "Cycles"
