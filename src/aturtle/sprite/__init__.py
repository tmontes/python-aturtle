# ----------------------------------------------------------------------------
# Python A-Turtle
# ----------------------------------------------------------------------------
# Copyright (c) Tiago Montes.
# See LICENSE for details.
# ----------------------------------------------------------------------------

from . vector import VectorSprite


def Sprite(canvas, shape, *, x=0, y=0, **kwargs):
    """
    """
    return VectorSprite(canvas, shape, x=x, y=y, **kwargs)
