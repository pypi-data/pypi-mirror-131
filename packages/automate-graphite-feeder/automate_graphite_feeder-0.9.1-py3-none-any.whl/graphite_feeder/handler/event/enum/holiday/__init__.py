import home

from graphite_feeder.handler.event.enum import Handler as Parent


class Handler(Parent):

    KLASS = home.event.holiday.Event
    TITLE = "San Silvester"

    def _get_url(self, name):
        url = 'target=alias(offset(keepLastValue({name}.{metric}), 0),"Over")&'.format(
            name=name, metric=self.metric
        )
        url += 'target=alias(offset(keepLastValue({name}.{metric}), 1),"Vacation")&'.format(
            name=name, metric=self.metric
        )
        return url


from graphite_feeder.handler.event.enum.holiday import christmas
from graphite_feeder.handler.event.enum.holiday import easter
from graphite_feeder.handler.event.enum.holiday import epiphany
from graphite_feeder.handler.event.enum.holiday import san_silvester
