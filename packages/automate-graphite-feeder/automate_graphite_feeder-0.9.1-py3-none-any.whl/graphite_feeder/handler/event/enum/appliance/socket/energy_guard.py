import home

from graphite_feeder.handler.event.enum.appliance import Handler as Parent


class Handler(Parent):

    KLASS = home.appliance.socket.event.forced.event.Event
