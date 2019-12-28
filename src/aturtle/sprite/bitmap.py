# ----------------------------------------------------------------------------
# Python A-Turtle
# ----------------------------------------------------------------------------
# Copyright (c) Tiago Montes.
# See LICENSE for details.
# ----------------------------------------------------------------------------

from . import base


class BitmapSprite(base.BaseSprite):

    def __init__(self, canvas, image, *, x=0, y=0):

        super().__init__(canvas, image, x=x, y=y)

        self._id = self._canvas.create_image(
            x - image.cx,
            y - image.cy,
            image=image[self._theta],
            anchor='nw',
        )


    def rotate(self, theta=0, *, around=None, update=False):

        # Rotate anchor point if needed.
        super().rotate(theta, around=around, update=False)

        # Anchor point rotated, move the image.
        if around:
            self._canvas.moveto(
                self._id,
                self._x_anchor - self._image.cx,
                self._y_anchor - self._image.cy,
            )

        # Use the pre-rendered image for the new orientation.
        self._canvas.itemconfig(self._id, image=self._image[self._theta])

        if update:
            self.update()
