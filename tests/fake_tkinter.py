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
        self._w = None
        self._h = None
        self.bind = mock.Mock()
        self.update = mock.Mock()
        self.destroy = mock.Mock()

    FULL_GEOMETRY_RE = re.compile(r'^(\d+)x(\d+)\+(\d+)\+(\d+)$')
    MOVE_GEOMETRY_RE = re.compile(r'^\+(\d+)\+(\d+)$')
    SIZE_GEOMETRY_RE = re.compile(r'^(\d+)x(\d+)$')

    def geometry(self, geometry):
        if full := self.FULL_GEOMETRY_RE.search(geometry):
            self._w, self._h, self._x, self._y = map(int, full.groups())
            return
        if move := self.MOVE_GEOMETRY_RE.search(geometry):
            self._x, self._y = map(int, move.groups())
            return
        if size := self.SIZE_GEOMETRY_RE.search(geometry):
            self._w, self._h = map(int, size.groups())


    def winfo_x(self):
        return self._x

    def winfo_y(self):
        return self._y

    def winfo_width(self):
        return self._w

    def winfo_height(self):
        return self._h



class FakeTk(FakeWindow):
    pass


class FakeToplevel(FakeWindow):
    pass


class FakeTkinter:

    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.Canvas = mock.Mock()

    def Tk(self):
        return FakeTk(self.screen_width, self.screen_height)

    def Toplevel(self):
        return FakeToplevel(self.screen_width, self.screen_height)
