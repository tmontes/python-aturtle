# ----------------------------------------------------------------------------
# Python A-Turtle
# ----------------------------------------------------------------------------
# Copyright (c) Tiago Montes.
# See LICENSE for details.
# ----------------------------------------------------------------------------

import itertools as it
import math

from . import base


class VectorSprite(base.BaseSprite):

    def __init__(self, canvas, image, *, x=0, y=0, fill_color='#009fff',
                 line_color='black', line_width=2):

        super().__init__(canvas, image, x=x, y=y)

        offset_coords = [
            value + offset
            for value, offset in zip(
                image.coords,
                it.cycle((x - image.x_anchor, y - image.y_anchor))
            )
        ]

        self._id = self._canvas.create_polygon(
            offset_coords,
            fill=fill_color,
            outline=line_color,
            width=line_width,
        )


    @property
    def coords(self):

        return self._canvas.coords(self._id)


    def rotate(self, theta=0, *, around=None, update=False):

        # Rotate anchor point if needed.
        super().rotate(theta, around=around, update=False)

        # Be fast
        sin_theta = math.sin(theta)
        cos_theta = math.cos(theta)
        cx = around[0] if around else self._x_anchor
        cy = around[1] if around else self._y_anchor

        # Avoid list reallocation
        coords = self._canvas.coords(self._id)
        for i in range(0, len(coords)-1, 2):
            x = coords[i] - cx
            y = coords[i+1] - cy
            coords[i] = x * cos_theta - y * sin_theta + cx
            coords[i+1] = x * sin_theta + y * cos_theta + cy

        self._canvas.coords(self._id, coords)
        if update:
            self.update()
