import home

from graphite_feeder.handler.event.appliance.str import Handler as Parent


class Handler(Parent):

    KLASS = home.appliance.sound.player.event.fade_out.playlist.Event
