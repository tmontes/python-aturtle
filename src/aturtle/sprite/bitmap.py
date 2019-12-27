# ----------------------------------------------------------------------------
# Python A-Turtle
# ----------------------------------------------------------------------------
# Copyright (c) Tiago Montes.
# See LICENSE for details.
# ----------------------------------------------------------------------------

import math
from . import base


class BitmapSprite(base.BaseSprite):

    def __init__(self, canvas, image, *, x=0, y=0):

        self._canvas = canvas
        self._id = None

        self._x_anchor = x
        self._y_anchor = y
        self._theta = 0

        self._image = image

        self._id = self._canvas.create_image(
            x - image.cx,
            y - image.cy,
            image=image[self._theta],
            anchor='nw',
        )


    @staticmethod
    def _anchor_offset(length, offset):

        return length * offset if isinstance(offset, float) else offset


    @property
    def x(self):

        return self._x_anchor


    @property
    def y(self):

        return self._y_anchor


    def move(self, dx=0, dy=0, *, update=False):

        self._x_anchor += dx
        self._y_anchor += dy
        self._canvas.move(self._id, dx, dy)
        if update:
            self.update()


    def moveto(self, x=0, y=0, *, update=False):

        self.move(x - self._x_anchor, y - self._y_anchor, update=update)


    def rotate(self, theta=0, *, around=None, update=False):

        self._theta = (self._theta + theta) % (math.pi * 2)

        # Use the pre-rendered image for the new orientation.
        self._canvas.itemconfig(self._id, image=self._image[self._theta])

        # Rotate anchor point, if not rotating around it.
        if around:
            cx, cy = around
            x = self._x_anchor - cx
            y = self._y_anchor - cy
            cos_theta = math.cos(theta)
            sin_theta = math.sin(theta)
            new_x = x * cos_theta - y * sin_theta + cx
            new_y = x * sin_theta + y * cos_theta + cy
            self._x_anchor = new_x
            self._y_anchor = new_y
            self._canvas.moveto(
                self._id,
                new_x - self._image.cx,
                new_y - self._image.cy,
            )

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
