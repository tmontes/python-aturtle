# ----------------------------------------------------------------------------
# Python A-Turtle
# ----------------------------------------------------------------------------
# Copyright (c) Tiago Montes.
# See LICENSE for details.
# ----------------------------------------------------------------------------

import tkinter

from . import base


class BitmapSprite(base.BaseSprite):

    def __init__(self, canvas, shape, *, x=0, y=0, x_anchor=0.5, y_anchor=0.5):

        self._canvas = canvas
        self._id = None

        try:
            image = tkinter.PhotoImage(file=shape)
        except tkinter.TclError as exc:
            raise IOError(exc)

        self._x_anchor = x
        self._y_anchor = y
        self._x_anchor_offset = self._anchor_offset(image.width(), x_anchor)
        self._y_anchor_offset = self._anchor_offset(image.height(), y_anchor)
        self._theta = 0

        self._image = image

        self._id = self._canvas.create_image(
            x - self._x_anchor_offset,
            y - self._y_anchor_offset,
            image=image,
            anchor=tkinter.NW,
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

        # TODO: Let's try this with the standard library only, shall we?
        raise NotImplementedError


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
