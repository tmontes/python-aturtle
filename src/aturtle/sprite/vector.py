# ----------------------------------------------------------------------------
# Python A-Turtle
# ----------------------------------------------------------------------------
# Copyright (c) Tiago Montes.
# See LICENSE for details.
# ----------------------------------------------------------------------------

import itertools as it

from . import base


class VectorSprite(base.BaseSprite):

    def __init__(self, canvas, shape, *, x=0, y=0):

        super().__init__(canvas, shape, x=x, y=y)

        self._id = self._canvas.create_polygon(
            self._offset_coords(0),
            fill=shape.fill_color,
            outline=shape.line_color,
            width=shape.line_width,
        )


    def _offset_coords(self, theta):

        return [
            value + offset
            for value, offset in zip(
                self._shape[theta],
                it.cycle((self._x_anchor, self._y_anchor))
            )
        ]


    @property
    def coords(self):

        return self._offset_coords(self._theta)


    def rotate(self, theta=0, *, around=None, update=False):

        # Rotate anchor point if needed.
        super().rotate(theta, around=around, update=False)

        # Use the shape for the new orientation.
        self._canvas.coords(
            self._id,
            self._offset_coords(self._theta),
        )
        if update:
            self.update()
