from abc import ABC, abstractmethod


class Graph(ABC):

    KLASS = None
    TITLE = "a title"
    LABEL = "a graph"
    METRIC = "state"
    MIN_MAX = True
    MIN = 0
    MAX = 1
    UNIT = ""
    FROM_NUMBER = "24"
    FROM_UNIT = "h"
    HIDE_Y_AXIS = "True"
    AREA_MODE = "all"
    CYAN = "209cee"
    MAGENTA = "dc20ee"
    RED = "ee2020"
    YELLOW = "eedf20"
    GREEN = "20ee2f"
    VIOLET = "7320ee"
    ORANGE = "ee8320"

    COLOR_LIST = "{},{},{},{},{},{},{}".format(
        CYAN, MAGENTA, VIOLET, ORANGE, YELLOW, RED, GREEN
    )

    @property
    def module(self):
        return self.KLASS.__module__

    @property
    def klass(self):
        return self.KLASS.__name__

    @property
    def unit(self):
        return self.UNIT

    @property
    def metric(self):
        return self.METRIC

    @property
    def title(self):
        return self.TITLE

    @property
    def label(self):
        return self.LABEL

    @property
    def min(self):
        return self.MIN

    @property
    def max(self):
        return self.MAX

    @property
    def hide_y_axis(self):
        return self.HIDE_Y_AXIS

    @property
    def area_mode(self):
        return self.AREA_MODE

    @property
    def color_list(self):
        return self.COLOR_LIST

    @property
    def from_number(self):
        if self._from_number:
            return self._from_number
        else:
            return self.FROM_NUMBER

    @property
    def from_unit(self):
        if self._from_unit:
            return self._from_unit
        else:
            return self.FROM_UNIT

    @abstractmethod
    def _get_url(self, name: str):
        ...

    def get_url(self, name: str):
        url = self._get_url(name)
        url += "areaMode={area_mode}&".format(area_mode=self.area_mode)
        url += "hideYAxis={hide_y_axis}&".format(hide_y_axis=self.hide_y_axis)
        url += "title={title}&".format(title=self.title)
        if self.MIN_MAX:
            url += "yMin={min}&".format(min=self.min)
            url += "yMax={max}&".format(max=self.max)
        url += "from=-{from_number}{from_unit}&".format(
            from_number=self.from_number, from_unit=self.from_unit
        )
        url += "colorList={color_list}".format(color_list=self.color_list)
        return url

    @abstractmethod
    def get_datapoint(self):
        ...
