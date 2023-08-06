from graphite_feeder.handler.event.int import Handler as Parent


class Handler(Parent):
    def get_datapoint(self):
        return self._event.value

    @property
    def metric(self):
        return self.module
