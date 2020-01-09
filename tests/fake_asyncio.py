# ----------------------------------------------------------------------------
# Python A-Turtle
# ----------------------------------------------------------------------------
# Copyright (c) Tiago Montes.
# See LICENSE for details.
# ----------------------------------------------------------------------------

from unittest import mock



class FakeAsyncio:

    class CancelledError(Exception):
        pass

    def __init__(self):

        self.sleep = mock.AsyncMock()
