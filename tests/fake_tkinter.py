# ----------------------------------------------------------------------------
# Python A-Turtle
# ----------------------------------------------------------------------------
# Copyright (c) Tiago Montes.
# See LICENSE for details.
# ----------------------------------------------------------------------------

import re
from unittest import mock



class FakeCanvas:

    def __init__(self, *args, **kwargs):
        self.init_args = mock.call(*args, **kwargs)
        self.pack = mock.Mock()
        self.config = mock.Mock()
        self.xview_scroll = mock.Mock()
        self.yview_scroll = mock.Mock()
        self.move = mock.Mock()
        self.coords = mock.Mock()
        self.update = mock.Mock()
        self.delete = mock.Mock()
        self.create_polygon = mock.Mock(return_value=42)
        self.create_image = mock.Mock(return_value=24)
        self.create_line = mock.Mock(return_value=42)
        self.itemconfig = mock.Mock()
        self.tag_lower = mock.Mock()
        self.tag_raise = mock.Mock()



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
        self.unbind = mock.Mock()
        self.after_idle = mock.Mock()
        self.after_cancel = mock.Mock()
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


class FakePhotoImage:

    def __init__(self):
        self.copies = 0
        self.width = mock.Mock(return_value=42)
        self.height = mock.Mock(return_value=24)
        self.get = mock.Mock(return_value=(10, 20, 30))
        self.put = mock.Mock()
        self.transparency_get = mock.Mock(return_value=False)
        self.transparency_set = mock.Mock()

    def copy(self):
        self.copies += 1
        return FakePhotoImage()



class FakeTkinter:

    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.windows = []
        self.canvases = []
        self.photoimage_init_calls = []

    def Tk(self):
        window = FakeTk(self.screen_width, self.screen_height)
        self.windows.append(window)
        return window

    def Toplevel(self):
        window = FakeToplevel(self.screen_width, self.screen_height)
        self.windows.append(window)
        return window

    def Canvas(self, *args, **kwargs):
        canvas = FakeCanvas(*args, **kwargs)
        self.canvases.append(canvas)
        return canvas

    def PhotoImage(self, *args, **kwargs):
        self.photoimage_init_calls.append((args, kwargs))
        return FakePhotoImage()
