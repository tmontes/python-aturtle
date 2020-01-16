# ----------------------------------------------------------------------------
# Python A-Turtle
# ----------------------------------------------------------------------------
# Copyright (c) Tiago Montes.
# See LICENSE for details.
# ----------------------------------------------------------------------------



class Turtle:

    def __init__(self, sprite, *, down=True):

        self._canvas = sprite.canvas
        self._sprite = sprite

        self._down = down

        self._line_id = None
        self._line_start = None
        self._lines = []


    def up(self):

        self._down = False


    def down(self):

        self._down = True


    def _sync_draw_line(self, _progress, anchor):

        if self._line_id:
            self._canvas.coords(self._line_id, *self._line_start, *anchor)
            # TODO: Improve this, cannot access private sprite attribute.
            self._canvas.tag_lower(self._line_id, self._sprite._id)
        else:
            self._line_id = self._canvas.create_line(*self._line_start, *anchor)
            self._lines.append(self._line_id)


    def sync_forward(self, distance):

        self._line_id = None
        self._line_start = self._sprite.anchor
        self._sprite.sync_forward(
            distance,
            callback=self._sync_draw_line if self._down else None,
        )
