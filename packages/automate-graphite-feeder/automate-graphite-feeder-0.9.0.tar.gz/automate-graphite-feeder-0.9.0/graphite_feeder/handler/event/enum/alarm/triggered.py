import home

from graphite_feeder.handler.event.enum import Handler as Parent


class Handler(Parent):

    KLASS = home.event.alarm.triggered.Event
    TITLE = "Alarm triggered"
