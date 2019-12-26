# ----------------------------------------------------------------------------
# Python A-Turtle
# ----------------------------------------------------------------------------
# Copyright (c) Tiago Montes.
# See LICENSE for details.
# ----------------------------------------------------------------------------

import pathlib

from . bitmap import BitmapSprite
from . vector import VectorSprite


def Sprite(canvas, shape, *, x=0, y=0, **kwargs):
    """
    """
    # If shape is a `str` or `Path`, take it as a filename with a bitmap image.
    if isinstance(shape, (pathlib.Path, str)):
        sprite = BitmapSprite(canvas, shape, x=x, y=y, **kwargs)
    else:
        sprite = VectorSprite(canvas, shape, x=x, y=y, **kwargs)

    return sprite
