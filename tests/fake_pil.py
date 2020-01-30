# ----------------------------------------------------------------------------
# Python A-Turtle
# ----------------------------------------------------------------------------
# Copyright (c) Tiago Montes.
# See LICENSE for details.
# ----------------------------------------------------------------------------

from unittest import mock


class PILImage:

    BICUBIC = object()

    init_calls = []

    def __init__(self, *args, **kwargs):
        type(self).init_calls.append((args, kwargs))
        self.width = 42
        self.height = 24

    @classmethod
    def open(cls, *args, **kwargs):
        return cls(*args, **kwargs)

    def convert(self, _format):
        return self

    rotate = mock.Mock()

    @classmethod
    def reset_after_tests(cls):
        cls.init_calls.clear()
        cls.rotate.reset_mock()


class PILImageTk:

    def __init__(self):
        self.photoimage_calls = []

    def PhotoImage(self, *args, **kwargs):
        self.photoimage_calls.append((args, kwargs))
