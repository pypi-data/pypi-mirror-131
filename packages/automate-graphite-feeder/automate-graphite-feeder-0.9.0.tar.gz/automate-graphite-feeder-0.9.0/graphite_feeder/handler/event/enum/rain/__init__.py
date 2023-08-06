import home

from graphite_feeder.handler.event.enum import Handler as Parent


class Handler(Parent):

    KLASS = home.event.rain.Event
    TITLE = "Rain"


from graphite_feeder.handler.event.enum.rain import forecast
from graphite_feeder.handler.event.enum.rain import in_the_past
