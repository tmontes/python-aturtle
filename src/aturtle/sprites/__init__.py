# ----------------------------------------------------------------------------
# Python A-Turtle
# ----------------------------------------------------------------------------
# Copyright (c) Tiago Montes.
# See LICENSE for details.
# ----------------------------------------------------------------------------

import pathlib

from ..shapes.bitmap import Shape as BitmapShape

from . bitmap import Sprite as BitmapSprite
from . vector import Sprite as VectorSprite


def Sprite(canvas, shape, *, anchor=(0, 0), **kwargs):
    """
    """
    if isinstance(shape, BitmapShape):
        sprite = BitmapSprite(canvas, shape, anchor=anchor, **kwargs)
    else:
        sprite = VectorSprite(canvas, shape, anchor=anchor, **kwargs)

    return sprite
