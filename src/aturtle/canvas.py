# ----------------------------------------------------------------------------
# Python A-Turtle
# ----------------------------------------------------------------------------
# Copyright (c) Tiago Montes.
# See LICENSE for details.
# ----------------------------------------------------------------------------

import tkinter



class InvertedYTkCanvas:

    def __init__(self, master, background):

        self._canvas = tkinter.Canvas(
            master,
            highlightthickness=0,
            background=background,
        )

    def _inverted_y(self, coords):

        return [
            -value if offset % 2 else value
            for offset, value in enumerate(coords)
        ]


    def create_polygon(self, coords, *, fill, outline, width):

        return self._canvas.create_polygon(
            self._inverted_y(coords),
            fill=fill,
            outline=outline,
            width=width,
        )


    def create_image(self, x, y, *, image, anchor):

        return self._canvas.create_image(x, -y, image=image, anchor=anchor)


    def create_line(self, coords, *, fill, width, capstyle):

        return self._canvas.create_line(
            self._inverted_y(coords),
            fill=fill,
            width=width,
            capstyle=capstyle,
        )


    def move(self, item_id, dx, dy):

        return self._canvas.move(item_id, dx, -dy)


    def coords(self, item_id, coords):

        return self._canvas.coords(item_id, self._inverted_y(coords))


    def __getattr__(self, name):

        return getattr(self._canvas, name)
