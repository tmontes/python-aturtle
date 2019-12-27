# ----------------------------------------------------------------------------
# Python A-Turtle
# ----------------------------------------------------------------------------
# Copyright (c) Tiago Montes.
# See LICENSE for details.
# ----------------------------------------------------------------------------

import pathlib

from aturtle import Bitmap

from . bitmap import BitmapSprite
from . vector import VectorSprite


def Sprite(canvas, image, *, x=0, y=0, **kwargs):
    """
    """
    if isinstance(image, Bitmap):
        sprite = BitmapSprite(canvas, image, x=x, y=y, **kwargs)
    else:
        sprite = VectorSprite(canvas, image, x=x, y=y, **kwargs)

    return sprite
