import home

from graphite_feeder.handler.appliance.sensor import Handler as Parent


class Handler(Parent):

    KLASS = home.appliance.sensor.luxmeter.Appliance
    TITLE = "Lux"

    def get_datapoint(self):
        return None
