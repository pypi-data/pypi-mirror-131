import home

from graphite_feeder.handler.event.enum.appliance import Handler as Parent


class Handler(Parent):

    KLASS = home.appliance.light.event.forced.event.Event


from graphite_feeder.handler.event.enum.appliance.light import indoor
