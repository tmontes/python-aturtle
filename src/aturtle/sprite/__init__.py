# ----------------------------------------------------------------------------
# Python A-Turtle
# ----------------------------------------------------------------------------
# Copyright (c) Tiago Montes.
# See LICENSE for details.
# ----------------------------------------------------------------------------

import pathlib

from . bitmap import BitmapSprite
from . vector import VectorSprite


def Sprite(canvas, image, *, x=0, y=0, **kwargs):
    """
    """
    # If `image.tk` exists, assume it is a `tkinter.PhotoImage`-like object.
    if hasattr(image, 'tk'):
        sprite = BitmapSprite(canvas, image, x=x, y=y, **kwargs)
    else:
        sprite = VectorSprite(canvas, image, x=x, y=y, **kwargs)

    return sprite
