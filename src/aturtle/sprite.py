# ----------------------------------------------------------------------------
# Python A-Turtle
# ----------------------------------------------------------------------------
# Copyright (c) Tiago Montes.
# See LICENSE for details.
# ----------------------------------------------------------------------------

import itertools as it
import math


class Sprite:

    def __init__(self, canvas, shape, *, x=0, y=0, fg='black', bg='#009fff',
                 lw=2, draw=True):

        self._c = canvas
        self._id = None

        self._x = x
        self._y = y
        self._theta = 0
        self._fg = fg
        self._bg = bg
        self._lw = lw

        self._xoffset = shape.x_center
        self._yoffset = shape.y_center

        offset_coords = [
            value - offset
            for value, offset in zip(
                shape.coords,
                it.cycle((shape.x_center, shape.y_center))
            )
        ]

        self._id = self._c.create_polygon(
            offset_coords,
            fill=self._bg,
            outline=self._fg,
            width=self._lw,
        )


    def coords(self):

        return self._c.coords(self._id)


    def move(self, dx=0, dy=0, *, update=False):

        self._x += dx
        self._y += dy
        self._c.move(self._id, dx, dy)
        if update:
            self.update()


    def moveto(self, x=0, y=0, *, update=False):

        self.move(x - self._x, y - self._y, update=update)


    def rotate(self, theta=0, *, around=None, update=False):

        # Be fast
        sin_theta = math.sin(theta)
        cos_theta = math.cos(theta)
        cx = around[0] if around else self._x
        cy = around[1] if around else self._y

        # Avoid list reallocation
        coords = self._c.coords(self._id)
        for i in range(0, len(coords)-1, 2):
            x = coords[i] - cx
            y = coords[i+1] - cy
            coords[i] = x * cos_theta - y * sin_theta + cx
            coords[i+1] = x * sin_theta + y * cos_theta + cy

        # Rotate anchor point, if not rotating around it.
        if around:
            x = self._x - cx
            y = self._y - cy
            new_x = x * cos_theta - y * sin_theta + cx
            new_y = x * sin_theta + y * cos_theta + cy
            self._x = new_x
            self._y = new_y

        self._c.coords(self._id, coords)
        self._theta += theta
        self._theta = self._theta % (math.pi * 2)
        if update:
            self.update()


    def unrotate(self, update=False):

        self.rotate(-self._theta, update=update)


    def update(self):

        # TODO: Use update_idletasks, instead?
        #       http://www.tcl.tk/man/tcl8.6/TclCmd/update.htm
        self._c.update()
    

    def delete(self):

        if self._id:
            self._c.delete(self._id)
            self._id = None
