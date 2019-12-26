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

    def __init__(self, canvas, shape, *, x=0, y=0, fill_color='#009fff',
                 line_color='black', line_width=2):

        self._canvas = canvas
        self._id = None

        self._x_anchor = x
        self._y_anchor = y
        self._theta = 0

        offset_coords = [
            value + offset
            for value, offset in zip(
                shape.coords,
                it.cycle((x - shape.x_anchor, y - shape.y_anchor))
            )
        ]

        self._id = self._canvas.create_polygon(
            offset_coords,
            fill=fill_color,
            outline=line_color,
            width=line_width,
        )


    @property
    def x(self):

        return self._x_anchor


    @property
    def y(self):

        return self._y_anchor


    @property
    def coords(self):

        return self._canvas.coords(self._id)


    def move(self, dx=0, dy=0, *, update=False):

        self._x_anchor += dx
        self._y_anchor += dy
        self._canvas.move(self._id, dx, dy)
        if update:
            self.update()


    def moveto(self, x=0, y=0, *, update=False):

        self.move(x - self._x_anchor, y - self._y_anchor, update=update)


    def rotate(self, theta=0, *, around=None, update=False):

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

        # Rotate anchor point, if not rotating around it.
        if around:
            x = self._x_anchor - cx
            y = self._y_anchor - cy
            new_x = x * cos_theta - y * sin_theta + cx
            new_y = x * sin_theta + y * cos_theta + cy
            self._x_anchor = new_x
            self._y_anchor = new_y

        self._canvas.coords(self._id, coords)
        self._theta = (self._theta + theta) % (math.pi * 2)
        if update:
            self.update()


    def unrotate(self, update=False):

        self.rotate(-self._theta, update=update)


    def update(self):

        # TODO: Use update_idletasks, instead?
        #       http://www.tcl.tk/man/tcl8.6/TclCmd/update.htm
        self._canvas.update()


    def delete(self):

        if self._id:
            self._canvas.delete(self._id)
            self._id = None
