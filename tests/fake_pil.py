# ----------------------------------------------------------------------------
# Python A-Turtle
# ----------------------------------------------------------------------------
# Copyright (c) Tiago Montes.
# See LICENSE for details.
# ----------------------------------------------------------------------------

class FakePILImage:

    init_calls = []

    def __init__(self, *args, **kwargs):
        type(self).init_calls.append((args, kwargs))

    @classmethod
    def open(cls, *args, **kwargs):
        return cls(*args, **kwargs)

    width = 42
    height = 24

    @classmethod
    def reset_after_tests(cls):
        cls.init_calls.clear()


class FakePILImageTk:
    pass
