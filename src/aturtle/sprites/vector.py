# ----------------------------------------------------------------------------
# Python A-Turtle
# ----------------------------------------------------------------------------
# Copyright (c) Tiago Montes.
# See LICENSE for details.
# ----------------------------------------------------------------------------

import itertools as it

from . import base


class Sprite(base.Sprite):

    def __init__(self, canvas, shape, *, anchor=(0, 0)):

        super().__init__(canvas, shape, anchor=anchor)

        self._id = self._canvas.create_polygon(
            self._offset_coords(0),
            fill=shape.fill_color,
            outline=shape.line_color,
            width=shape.line_width,
        )


    def _offset_coords(self, theta):

        shape_coords = self._shape[theta]
        anchor_cycle = it.cycle(self._anchor)
        return [
            value + offset
            for value, offset in zip(shape_coords, anchor_cycle)
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
