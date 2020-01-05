# ----------------------------------------------------------------------------
# Python A-Turtle
# ----------------------------------------------------------------------------
# Copyright (c) Tiago Montes.
# See LICENSE for details.
# ----------------------------------------------------------------------------

import itertools as it

from . import base


class Sprite(base.Sprite):

    def __init__(self, canvas, shape, *, anchor=(0, 0), angle=0):

        super().__init__(canvas, shape, anchor=anchor, angle=angle)

        self._id = self._canvas.create_polygon(
            self._offset_shape_coords(angle),
            fill=shape.fill_color,
            outline=shape.line_color,
            width=shape.line_width,
        )


    def _offset_shape_coords(self, angle):

        shape_coords = self._shape[angle]
        anchor_cycle = it.cycle(self._anchor)
        return [
            value + offset
            for value, offset in zip(shape_coords, anchor_cycle)
        ]


    @property
    def coords(self):

        return self._offset_shape_coords(self._angle)


    def rotate(self, angle=0, *, around=None, update=False):

        # Rotate anchor point if needed.
        super().rotate(angle, around=around, update=False)

        # Use the shape for the new orientation.
        self._canvas.coords(
            self._id,
            self._offset_shape_coords(self._angle),
        )
        if update:
            self.update()
