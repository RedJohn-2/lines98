from Size import Size
from Color import Color


class Ball:

    def __init__(self, size, color):
        self._size = size
        self._color = color

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, size: Size):
        self._size = size

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, color: Color):
        self._color = color

    def __eq__(self, o: object) -> bool:
        if isinstance(o, Ball):
            return self._size == o.size and self._color == o.color

