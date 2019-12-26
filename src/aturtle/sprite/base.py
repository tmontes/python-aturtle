# ----------------------------------------------------------------------------
# Python A-Turtle
# ----------------------------------------------------------------------------
# Copyright (c) Tiago Montes.
# See LICENSE for details.
# ----------------------------------------------------------------------------


class BaseSprite:

    """
    Base class.
    """

    def __init__(self, canvas, shape, *, x=0, y=0):
        """
        Initialize a Sprite with the given `shape` and draw it on the output
        `canvas` at (`x`, `y`).
        """
        raise NotImplementedError


    @property
    def x(self):
        """
        The Sprite's `x` position in the canvas.
        """
        raise NotImplementedError


    @property
    def y(self):
        """
        The Sprite's `y` position in the canvas.
        """
        raise NotImplementedError


    def move(self, dx=0, dy=0, *, update=False):
        """
        Move the Sprite by the given relative `dx` and `dy` values.
        Update the output if `update` is true.
        """
        raise NotImplementedError


    def moveto(self, x=0, y=0, *, update=False):
        """
        Move the Sprite to the given absolute (`x`, `y`) position.
        Update the output if `update` is true.
        """
        raise NotImplementedError


    def rotate(self, theta=0, *, around=None, update=False):
        """
        Rotate the Sprite by `theta` radians. If `around` is None, rotate it
        around itself, otherwise, rotate it about `around`, assumued to be a
        (cx, cy) two-tuple defining the center of rotation.
        Update the output if `update` is true.
        """
        raise NotImplementedError


    def unrotate(self, update=False):
        """
        Undo any previous rotation. Update the output if `update` is true.
        """
        raise NotImplementedError


    def update(self):
        """
        Update the the output by redrawing pending movements or rotations.
        """
        raise NotImplementedError


    def delete(self):
        """
        Remove the Sprite from the output, getting ready for object deletion.
        """
        raise NotImplementedError
