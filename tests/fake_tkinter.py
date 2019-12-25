# ----------------------------------------------------------------------------
# Python A-Turtle
# ----------------------------------------------------------------------------
# Copyright (c) Tiago Montes.
# See LICENSE for details.
# ----------------------------------------------------------------------------

import collections
import re
from unittest import mock


class FakeWindow:

    def __init__(self, screen_width, screen_height):
        self.winfo_screenwidth = mock.Mock(return_value=screen_width)
        self.winfo_screenheight = mock.Mock(return_value=screen_height)
        self.title = mock.Mock()
        self._x = None
        self._y = None
        self._width = None
        self._height = None
        self.bind = mock.Mock()
        self.update = mock.Mock()
        self.destroy = mock.Mock()

    GEOMETRY_RE = re.compile(r'(\d+)x(\d+)\+(\d+)\+(\d+)')

    def geometry(self, geometry):
        match = self.GEOMETRY_RE.search(geometry)
        width, height, x, y = map(int, match.groups())
        self._x = x
        self._y = y
        self._width = width
        self._height = height

    def winfo_x(self):
        return self._x

    def winfo_y(self):
        return self._y

    def winfo_width(self):
        return self._width

    def winfo_height(self):
        return self._height



class FakeTk(FakeWindow):
    pass


class FakeToplevel(FakeWindow):
    pass


class FakeTkinter:

    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.tk_calls = 0
        self.toplevel_calls = 0
        self.Canvas = mock.Mock()

    def Tk(self):
        self.tk_calls += 1
        return FakeTk(self.screen_width, self.screen_height)

    def Toplevel(self):
        self.toplevel_calls += 1
        return FakeToplevel(self.screen_width, self.screen_height)
