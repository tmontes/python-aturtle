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

    def pack(self, *, expand, fill):

        return self._canvas.pack(expand=expand, fill=fill)


    def config(self, *, xscrollincrement, yscrollincrement):

        return self._canvas.config(
            xscrollincrement=xscrollincrement,
            yscrollincrement=yscrollincrement,
        )


    def xview_scroll(self, number, what):

        return self._canvas.xview_scroll(number, what)


    def yview_scroll(self, number, what):

        return self._canvas.yview_scroll(number, what)



    def itemconfig(self, item_id, *, image):

        return self._canvas.itemconfig(item_id, image=image)


    def update(self):

        return self._canvas.update()


    def tag_raise(self, item_id, other=None):

        return self._canvas.tag_raise(item_id, other)


    def tag_lower(self, item_id, other=None):

        return self._canvas.tag_lower(item_id, other)


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


    def delete(self, item_id):

        return self._canvas.delete(item_id)
