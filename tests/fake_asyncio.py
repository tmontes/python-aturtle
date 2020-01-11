# ----------------------------------------------------------------------------
# Python A-Turtle
# ----------------------------------------------------------------------------
# Copyright (c) Tiago Montes.
# See LICENSE for details.
# ----------------------------------------------------------------------------

from unittest import mock



class FakeSleep:

    def __await__(self):
        yield


class FakeAsyncio:

    class CancelledError(Exception):
        pass

    def __init__(self):
        self.sleep_call_args = []

    def sleep(self, seconds):
        self.sleep_call_args.append(seconds)
        return FakeSleep()
