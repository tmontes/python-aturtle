# ----------------------------------------------------------------------------
# Python A-Turtle
# ----------------------------------------------------------------------------
# Copyright (c) Tiago Montes.
# See LICENSE for details.
# ----------------------------------------------------------------------------

import pathlib

from ..shapes.bitmap import Shape as _BitmapShape
from ..shapes.vector import Shape as _VectorShape

from . bitmap import Sprite as BitmapSprite
from . vector import Sprite as VectorSprite



def create_sprite(target, shape_source, *, anchor=(0, 0), angle=0,
                  speed=360, m_speed=None, r_speed=None,
                  easing=None, m_easing=None, r_easing=None,
                  m_callback=None, r_callback=None,
                  fps=80, update=False, **kwargs):
    """
    Returns a newly created sprite from `shape_source`, placed at the `anchor`
    position in the given `target`, which should be either an aturtle.Window
    object or a tkinter.Canvas one.

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
    canvas = target.canvas if hasattr(target, 'canvas') else target
    if isinstance(shape_source, (str, pathlib.Path)):
        shape = _BitmapShape(filename=shape_source, **kwargs)
        sprite = BitmapSprite(canvas, shape, anchor=anchor, angle=angle,
                              speed=speed, m_speed=m_speed, r_speed=r_speed,
                              easing=easing, m_easing=m_easing, r_easing=r_easing,
                              m_callback=m_callback, r_callback=r_callback,
                              fps=fps, update=update)
    elif isinstance(shape_source, bytes):
        shape = _BitmapShape(data=shape_source, **kwargs)
        sprite = BitmapSprite(canvas, shape, anchor=anchor, angle=angle,
                              speed=speed, m_speed=m_speed, r_speed=r_speed,
                              easing=easing, m_easing=m_easing, r_easing=r_easing,
                              m_callback=m_callback, r_callback=r_callback,
                              fps=fps, update=update)
    elif isinstance(shape_source, list):
        shape = _VectorShape(shape_source, **kwargs)
        sprite = VectorSprite(canvas, shape, anchor=anchor, angle=angle,
                              speed=speed, m_speed=m_speed, r_speed=r_speed,
                              easing=easing, m_easing=m_easing, r_easing=r_easing,
                              m_callback=m_callback, r_callback=r_callback,
                              fps=fps, update=update)
    elif isinstance(shape_source, _VectorShape):
        sprite = VectorSprite(canvas, shape_source, anchor=anchor, angle=angle,
                              speed=speed, m_speed=m_speed, r_speed=r_speed,
                              easing=easing, m_easing=m_easing, r_easing=r_easing,
                              m_callback=m_callback, r_callback=r_callback,
                              fps=fps, update=update)
    elif isinstance(shape_source, _BitmapShape):
        sprite = BitmapSprite(canvas, shape_source, anchor=anchor, angle=angle,
                              speed=speed, m_speed=m_speed, r_speed=r_speed,
                              easing=easing, m_easing=m_easing, r_easing=r_easing,
                              m_callback=m_callback, r_callback=r_callback,
                              fps=fps, update=update)
    else:
        raise TypeError(f'Unhandled shape_source type: {type(shape_source)}.')

    return sprite
