import home

from graphite_feeder.handler.event.appliance.str import Handler as Parent


class Handler(Parent):

    KLASS = home.appliance.sound.player.event.forced.circadian_rhythm.playlist_a.Event
