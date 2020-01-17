# ----------------------------------------------------------------------------
# Python A-Turtle
# ----------------------------------------------------------------------------
# Copyright (c) Tiago Montes.
# See LICENSE for details.
# ----------------------------------------------------------------------------

from . utils import syncer



_LINE_COLOR = '#cccccc'
_LINE_WIDTH = 3



class Turtle:

    def __init__(self, sprite, *, down=True, line_color=_LINE_COLOR,
                 line_width=_LINE_WIDTH):

        self._canvas = sprite.canvas
        self._sprite = sprite

        self._down = down
        self.line_color = line_color
        self.line_width = line_width

        self._line_id = None
        self._line_start = None
        self._lines = []


    def up(self):

        self._down = False


    def down(self):

        self._down = True


    async def _async_draw_line(self, _progress, anchor):

        if self._line_id:
            self._canvas.coords(self._line_id, *self._line_start, *anchor)
        else:
            self._line_id = self._canvas.create_line(
                *self._line_start,
                *anchor,
                fill=self.line_color,
                width=self.line_width,
                capstyle='round',
            )
            # TODO: Improve this, cannot access private sprite attribute.
            self._canvas.tag_lower(self._line_id, self._sprite._id)
            self._lines.append(self._line_id)


    async def async_forward(self, distance):

        self._line_id = None
        self._line_start = self._sprite.anchor
        await self._sprite.async_forward(
            distance,
            callback=self._async_draw_line if self._down else None,
        )


    async def async_left(self, angle):

        await self._sprite.async_rotate(-angle)


    async def async_right(self, angle):

        await self._sprite.async_rotate(angle)


    def name_mapper(name):
        if name.startswith('_async'):
            return '_' + name[2:]
        if name.startswith('async'):
            return name[1:]
        return name

    _sync_draw_line = syncer.create_sync_func(_async_draw_line, name_mapper)
    sync_forward = syncer.create_sync_func(async_forward, name_mapper)
    sync_left = syncer.create_sync_func(async_left, name_mapper)
    sync_right = syncer.create_sync_func(async_right, name_mapper)

    del name_mapper
