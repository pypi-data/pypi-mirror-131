import home

from graphite_feeder.handler.event.appliance.sound.player.volume import (
    Handler as Parent,
)


class Handler(Parent):

    KLASS = home.appliance.sound.player.event.fade_out.volume.Event
    TITLE = "Fade out volume (%)"
