# ----------------------------------------------------------------------------
# Python A-Turtle
# ----------------------------------------------------------------------------
# Copyright (c) Tiago Montes.
# See LICENSE for details.
# ----------------------------------------------------------------------------

import math


class BaseSprite:

    """
    Base class.
    """

    def __init__(self, canvas, shape, *, x=0, y=0):
        """
        Initialize a Sprite with the given `shape` and place it on the output
        `canvas` at the given `x`, `y` coordinates.
        """
        self._canvas = canvas
        self._id = None

        self._shape = shape
        self._x_anchor = x
        self._y_anchor = y
        self._theta = 0


    @property
    def x(self):
        """
        The Sprite's `x` position in the canvas.
        """
        return self._x_anchor


    @property
    def y(self):
        """
        The Sprite's `y` position in the canvas.
        """
        return self._y_anchor


    def move(self, dx=0, dy=0, *, update=False):
        """
        Move the Sprite by the given relative `dx` and `dy` values.
        Update the output if `update` is true.
        """
        self._x_anchor += dx
        self._y_anchor += dy
        self._canvas.move(self._id, dx, dy)
        if update:
            self.update()


    def moveto(self, x=0, y=0, *, update=False):
        """
        Move the Sprite to the given absolute (`x`, `y`) position.
        Update the output if `update` is true.
        """
        self.move(x - self._x_anchor, y - self._y_anchor, update=update)


    def rotate(self, theta=0, *, around=None, update=False):
        """
        Rotate the Sprite anchor by `theta` radians. If `around` is None, the
        anchor is left unchanged. Otherwise, rotate it about `around`, assumed
        to be a (cx, cy) two-tuple defining the center of rotation.
        Update the output if `update` is true.
        """
        self._theta = (self._theta + theta) % (math.pi * 2)
        if around:
            cx, cy = around
            x = self._x_anchor - cx
            y = self._y_anchor - cy
            sin_theta = math.sin(theta)
            cos_theta = math.cos(theta)
            new_x = x * cos_theta - y * sin_theta + cx
            new_y = x * sin_theta + y * cos_theta + cy
            self._x_anchor = new_x
            self._y_anchor = new_y
        if update:
            self.update()


    def unrotate(self, update=False):
        """
        Undo any previous rotation. Update the output if `update` is true.
        """
        self.rotate(-self._theta, update=update)


    def update(self):
        """
        Update the the output by redrawing pending movements or rotations.
        """
        # TODO: Use update_idletasks, instead?
        #       http://www.tcl.tk/man/tcl8.6/TclCmd/update.htm
        self._canvas.update()


    def delete(self):
        """
        Remove the Sprite from the output, getting ready for object deletion.
        """
        if self._id:
            self._canvas.delete(self._id)
            self._id = None
