# ----------------------------------------------------------------------------
# Python A-Turtle
# ----------------------------------------------------------------------------
# Copyright (c) Tiago Montes.
# See LICENSE for details.
# ----------------------------------------------------------------------------

from unittest import mock



class Sprite:

    def __init__(self, canvas, anchor, angle):
        self.canvas = canvas
        self.anchor = anchor
        self.angle = angle
        self.async_move = mock.AsyncMock()
        self.async_move_to = mock.AsyncMock()
        self.async_forward = mock.AsyncMock()
        self.async_rotate = mock.AsyncMock()
        self.sync_move = mock.Mock()
        self.sync_move_to = mock.Mock()
        self.sync_forward = mock.Mock()
        self.sync_rotate = mock.Mock()
