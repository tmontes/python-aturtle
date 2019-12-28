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


def Sprite(canvas, shape, *, x=0, y=0, **kwargs):
    """
    """
    if isinstance(shape, Bitmap):
        sprite = BitmapSprite(canvas, shape, x=x, y=y, **kwargs)
    else:
        sprite = VectorSprite(canvas, shape, x=x, y=y, **kwargs)

    return sprite
