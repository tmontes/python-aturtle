# ----------------------------------------------------------------------------
# Python A-Turtle
# ----------------------------------------------------------------------------
# Copyright (c) Tiago Montes.
# See LICENSE for details.
# ----------------------------------------------------------------------------

import tkinter



class InvertedYCanvas:

    """
    Behaves like a tkinter.Canvas widget, where Y coordinates are negated such
    that larger values are at the top of the screen.
    """

    def __init__(self, master, background):
        """
        Creates a Canvas widget with parent `master` and the given `background`
        color. Sets the underlying tkinter.Canvas widget's highlightthickness
        to zero such that no border/outline is visible.
        """
        self._canvas = tkinter.Canvas(
            master,
            highlightthickness=0,
            background=background,
        )

    def _inverted_y(self, coords):

        # `coords` is an iterable of (x0, y0, x1, y0, ..., xn, yn) numbers,
        # where the ones in odd offsets/indices are Y values that are negated.

        return [
            -value if offset % 2 else value
            for offset, value in enumerate(coords)
        ]


    def create_polygon(self, coords, *, fill, outline, width):
        """
        Creates a polygon item with given `coords` and visual attributes.
        """
        return self._canvas.create_polygon(
            self._inverted_y(coords),
            fill=fill,
            outline=outline,
            width=width,
        )


    def create_image(self, x, y, *, image, anchor):
        """
        Creates an image item at the given (`x`, `y`) position with the `image`
        achored at `anchor`.
        """
        return self._canvas.create_image(x, -y, image=image, anchor=anchor)


    def create_line(self, coords, *, fill, width, capstyle):
        """
        Creates a line item with given `coords` and visual attributes.
        """
        return self._canvas.create_line(
            self._inverted_y(coords),
            fill=fill,
            width=width,
            capstyle=capstyle,
        )


    def move(self, item_id, dx, dy):
        """
        Moves the item identified by `item_id` relatively by (`dx`, `dy`).
        """
        return self._canvas.move(item_id, dx, -dy)


    def coords(self, item_id, coords):
        """
        Sets the coordinates of the item identified by `item_id` to `coords`.
        """
        return self._canvas.coords(item_id, self._inverted_y(coords))


    def __getattr__(self, name):
        """
        Delegates attribute access to the wrapped tkinter.Canvas object.
        """
        return getattr(self._canvas, name)
