# ----------------------------------------------------------------------------
# Python A-Turtle
# ----------------------------------------------------------------------------
# Copyright (c) Tiago Montes.
# See LICENSE for details.
# ----------------------------------------------------------------------------

import pathlib

from ..shapes.bitmap import Shape as BitmapShape
from ..shapes.vector import Shape as VectorShape

from . bitmap import Sprite as BitmapSprite
from . vector import Sprite as VectorSprite



def create_sprite(canvas, shape_source, *, anchor=(0, 0), **kwargs):
    """
    Returns a newly created sprite from `shape_source`, placed at the `anchor`
    position in the given `canvas`.

    The sprite's type and shape depend on the type of `shape_source`:

    - A `str` or `pathlib.Path` represents a file with bitmap image data.
      An underlying bitmap shape is created and used for the sprite.
    - A `bytes` object represents base-64 encoded bitmap image data.
      An underlying bitmap shape is created and used for the sprite.
    - A `list` represents a sequence of coorinates as in [x1, y1, x2, y2, ...].
      An underlying vector shape is created and used for the sprite.
    - A `aturtle.shapes.vector.Shape` or a `aturtle.shapes.bitmap.Shape` are
      used directly, with no underlying shape creation taking place.

    Additional arguments are passed as-is when creating an underlying shape.
    Note that it is not possible to pass an `anchor` argument to such shapes:
    for that, such a customized shape must be created beforehand and passed in
    explicitly via `shape_source`.
    """
    if isinstance(shape_source, (str, pathlib.Path)):
        shape = BitmapShape(filename=shape_source, **kwargs)
        sprite = BitmapSprite(canvas, shape, anchor=anchor)
    elif isinstance(shape_source, bytes):
        shape = BitmapShape(data=shape_source, **kwargs)
        sprite = BitmapSprite(canvas, shape, anchor=anchor)
    elif isinstance(shape_source, list):
        shape = VectorShape(shape_source, **kwargs)
        sprite = VectorSprite(canvas, shape, anchor=anchor)
    elif isinstance(shape_source, VectorShape):
        sprite = VectorSprite(canvas, shape_source, anchor=anchor)
    elif isinstance(shape_source, BitmapShape):
        sprite = BitmapSprite(canvas, shape_source, anchor=anchor)
    else:
        raise ValueError(f'Unhandled shape_source type: {type(shape_source)}.')

    return sprite
