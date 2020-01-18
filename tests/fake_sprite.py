# ----------------------------------------------------------------------------
# Python A-Turtle
# ----------------------------------------------------------------------------
# Copyright (c) Tiago Montes.
# See LICENSE for details.
# ----------------------------------------------------------------------------

from unittest import mock



class FakeSprite:

    def __init__(self, canvas, anchor, angle):
        self.canvas = canvas
        self.anchor = anchor
        self.angle = angle
        self.async_rotate = mock.AsyncMock()
        self.sync_rotate = mock.Mock()
