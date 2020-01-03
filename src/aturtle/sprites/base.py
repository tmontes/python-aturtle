# ----------------------------------------------------------------------------
# Python A-Turtle
# ----------------------------------------------------------------------------
# Copyright (c) Tiago Montes.
# See LICENSE for details.
# ----------------------------------------------------------------------------

import math


class Sprite:

    """
    Base class.
    """

    def __init__(self, canvas, shape, *, anchor=(0, 0), angle=0):
        """
        Initialize a Sprite with the given `shape` and place it on the output
        `canvas` at the given `x`, `y` coordinates, rotated `angle` degrees.
        """
        self._canvas = canvas
        self._id = None

        self._shape = shape
        self._anchor = anchor
        self._angle = angle


    @property
    def anchor(self):
        """
        The Sprite's anchor position in the canvas, as an (x, y) tuple.
        """
        return self._anchor


    @property
    def angle(self):
        """
        The Sprite's rotation angle, in degrees.
        """
        return self._angle


    def move(self, dx=0, dy=0, *, update=False):
        """
        Move the Sprite by the given relative `dx` and `dy` values.
        Update the output if `update` is true.
        """
        sprite_x, sprite_y = self._anchor
        self._anchor = (sprite_x + dx, sprite_y + dy)
        self._canvas.move(self._id, dx, dy)
        if update:
            self.update()


    def move_to(self, x=0, y=0, *, update=False):
        """
        Move the Sprite to the given absolute (`x`, `y`) position.
        Update the output if `update` is true.
        """
        sprite_x, sprite_y = self._anchor
        self.move(x - sprite_x, y - sprite_y, update=update)


    def rotate(self, angle=0, *, around=None, update=False):
        """
        Rotate the Sprite anchor by `angle` degrees. If `around` is None, the
        anchor is left unchanged. Otherwise, rotate it about `around`, assumed
        to be a (cx, cy) two-tuple defining the center of rotation.
        Update the output if `update` is true.
        """
        self._angle = (self._angle + angle) % 360
        angle_rad = angle * math.pi / 180.0
        if around:
            sprite_x, sprite_y = self._anchor
            cx, cy = around
            sprite_x -= cx
            sprite_y -= cy
            sin_theta = math.sin(angle_rad)
            cos_theta = math.cos(angle_rad)
            new_x = sprite_x * cos_theta - sprite_y * sin_theta + cx
            new_y = sprite_x * sin_theta + sprite_y * cos_theta + cy
            self._anchor = (new_x, new_y)
        if update:
            self.update()


    def rotate_to(self, angle=0, around=None, update=False):
        """
        Rotate the Sprite anchor to `angle` degrees, with 0 being the
        underlying shape's original orientation. If `anchor` is None,
        the anchor is left unchanged. Otherwise, it is rotated around
        it, assumed to be a (cx, cy) two-tuple defining the center of
        rotation.
        Update the output if `update` is true.
        """
        self.rotate(angle-self._angle, around=around, update=update)


    def update(self):
        """
        Update the the output by redrawing pending movements or rotations.
        """
        self._canvas.update_idletasks()


    def delete(self):
        """
        Remove the Sprite from the output, getting ready for object deletion.
        """
        if self._id:
            self._canvas.delete(self._id)
            self._id = None
