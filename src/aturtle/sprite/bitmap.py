# ----------------------------------------------------------------------------
# Python A-Turtle
# ----------------------------------------------------------------------------
# Copyright (c) Tiago Montes.
# See LICENSE for details.
# ----------------------------------------------------------------------------

from . import base


class BitmapSprite(base.BaseSprite):

    def __init__(self, canvas, shape, *, x=0, y=0):

        super().__init__(canvas, shape, x=x, y=y)

        self._id = self._canvas.create_image(
            x - shape.cx,
            y - shape.cy,
            image=shape[self._theta],
            anchor='nw',
        )


    def rotate(self, theta=0, *, around=None, update=False):

        # Rotate anchor point if needed.
        super().rotate(theta, around=around, update=False)

        # Anchor point rotated, move the shape.
        if around:
            self._canvas.moveto(
                self._id,
                self._x_anchor - self._shape.cx,
                self._y_anchor - self._shape.cy,
            )

        # Use the pre-rendered shape for the new orientation.
        self._canvas.itemconfig(self._id, image=self._shape[self._theta])

        if update:
            self.update()
