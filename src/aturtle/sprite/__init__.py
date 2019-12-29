# ----------------------------------------------------------------------------
# Python A-Turtle
# ----------------------------------------------------------------------------
# Copyright (c) Tiago Montes.
# See LICENSE for details.
# ----------------------------------------------------------------------------

import pathlib

from ..shapes import Bitmap

from . bitmap import BitmapSprite
from . vector import VectorSprite


def Sprite(canvas, shape, *, anchor=(0, 0), **kwargs):
    """
    """
    if isinstance(shape, Bitmap):
        sprite = BitmapSprite(canvas, shape, anchor=anchor, **kwargs)
    else:
        sprite = VectorSprite(canvas, shape, anchor=anchor, **kwargs)

    return sprite
