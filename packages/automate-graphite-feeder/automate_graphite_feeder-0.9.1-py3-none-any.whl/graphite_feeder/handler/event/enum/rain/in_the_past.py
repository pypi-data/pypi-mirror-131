import home

from graphite_feeder.handler.event.enum.rain import Handler as Parent


class Handler(Parent):

    KLASS = home.event.rain.in_the_past.Event
    TITLE = "Has rained"
