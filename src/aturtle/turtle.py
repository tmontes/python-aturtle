# ----------------------------------------------------------------------------
# Python A-Turtle
# ----------------------------------------------------------------------------
# Copyright (c) Tiago Montes.
# See LICENSE for details.
# ----------------------------------------------------------------------------



class Turtle:

    def __init__(self, sprite, *, drawing=True):

        self._canvas = sprite.canvas
        self._sprite = sprite

        self._drawing = drawing

        self._line_id = None
        self._line_start = None
        self._lines = []


    def _draw_line(self, _progress, anchor):

        if self._line_id:
            self._canvas.coords(self._line_id, *self._line_start, *anchor)
            self._canvas.tag_lower(self._line_id, self._sprite._id)
        else:
            self._line_id = self._canvas.create_line(*self._line_start, *anchor)
            self._lines.append(self._line_id)


    def sync_forward(self, distance):

        self._line_id = None
        self._line_start = self._sprite.anchor
        self._sprite.sync_forward(
            distance,
            callback=self._draw_line if self._drawing else None,
        )
