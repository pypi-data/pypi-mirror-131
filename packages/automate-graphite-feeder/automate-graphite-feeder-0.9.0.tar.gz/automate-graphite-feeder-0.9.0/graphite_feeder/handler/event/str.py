from graphite_feeder.handler.event import handler


class Handler(handler.Handler):
    """
    Do not return a graph for str events!
    """

    def _get_url(self, name):
        return None

    def get_datapoint(self):
        return 0
