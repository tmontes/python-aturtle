# ----------------------------------------------------------------------------
# Python A-Turtle
# ----------------------------------------------------------------------------
# Copyright (c) Tiago Montes.
# See LICENSE for details.
# ----------------------------------------------------------------------------

from unittest import mock



class Sleep:

    def __await__(self):
        yield


class Asyncio:

    class CancelledError(Exception):
        pass

    def __init__(self):
        self.sleep_call_args = []

    def sleep(self, seconds):
        self.sleep_call_args.append(seconds)
        return Sleep()
