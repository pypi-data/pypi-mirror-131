from graphite_feeder.handler.event import handler


class Handler(handler.Handler):

    KLASS = int
    TITLE = "Value"
    METRIC = "int"
    HIDE_Y_AXIS = False
    MIN_MAX = False
    AREA_MODE = "none"

    def _get_url(self, name):
        url = "target=keepLastValue({name}.{metric})&lineMode=staircase&hideLegend=True&lineWidth=2&".format(
            name=name, metric=self.metric
        )
        return url

    def get_datapoint(self):
        return self._event
