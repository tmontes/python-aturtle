# ----------------------------------------------------------------------------
# Python A-Turtle
# ----------------------------------------------------------------------------
# Copyright (c) Tiago Montes.
# See LICENSE for details.
# ----------------------------------------------------------------------------

import tkinter



class InvertedYTkCanvas(tkinter.Canvas):

    def __init__(self, master, background):

        super().__init__(
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

        return super().create_polygon(
            self._inverted_y(coords),
            fill=fill,
            outline=outline,
            width=width,
        )


    def move(self, item_id, dx, dy):

        return super().move(item_id, dx, -dy)


    def create_line(self, coords, *, fill, width, capstyle):

        return super().create_line(
            self._inverted_y(coords),
            fill=fill,
            width=width,
            capstyle=capstyle,
        )


    def coords(self, item_id, coords):

        return super().coords(item_id, self._inverted_y(coords))

