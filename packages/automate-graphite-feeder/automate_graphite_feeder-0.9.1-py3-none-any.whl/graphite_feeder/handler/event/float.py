from graphite_feeder.handler.event.int import Handler as Parent


class Handler(Parent):

    KLASS = float
    METRIC = "float"

    def get_datapoint(self):
        return self._event
