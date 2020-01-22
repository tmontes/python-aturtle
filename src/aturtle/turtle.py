# ----------------------------------------------------------------------------
# Python A-Turtle
# ----------------------------------------------------------------------------
# Copyright (c) Tiago Montes.
# See LICENSE for details.
# ----------------------------------------------------------------------------

import contextlib

from . utils import syncer



_LINE_COLOR = '#cccccc'
_LINE_WIDTH = 3



class Turtle:

    """
    A line drawing Turtle.
    """

    def __init__(self, sprite, *, down=True, line_color=_LINE_COLOR,
                 line_width=_LINE_WIDTH):
        """
        Initialize Turtle to be visually represented with the given `sprite`.

        When `down` is true, turtle movements draw lines on the `sprite`'s
        canvas, following its movement. No lines are drawn otherwise.

        Lines are drawn in the given `line_color` and `line_width`.
        """

        self._canvas = sprite.canvas
        self._sprite = sprite

        self.down = down
        self.line_color = line_color
        self.line_width = line_width

        self._line_id = None
        self._line_coords = None
        self._lines = []


    @property
    def anchor(self):
        """
        The turtle's anchor position in the canvas, as an (x, y) tuple.
        """
        return self._sprite.anchor


    @property
    def angle(self):
        """
        The turtle's rotation angle, in degrees.
        """
        return self._sprite.angle


    @contextlib.contextmanager
    def _down_override(self, down):

        save_down = self.down
        if down is not None:
            self.down = down

        try:
            yield
        finally:
            self.down = save_down


    async def _async_draw_line(self, _progress, anchor):
        """
        Sprite movement callback to handle line drawing.
        """
        self._line_coords.extend(anchor)
        if self._line_id:
            self._canvas.coords(self._line_id, self._line_coords)
        else:
            self._line_id = self._canvas.create_line(
                self._line_coords,
                fill=self.line_color,
                width=self.line_width,
                capstyle='round',
            )
            self._sprite.to_front(of=self._line_id)
            self._lines.append(self._line_id)


    async def async_forward(self, delta, *, down=None, track_angle=True,
                            speed=None, easing=None, fps=None, update=None):
        """
        Animated move of the Turtle forward by `delta` in the direction set by
        its angle. Negative values move in the opposite direction.

        The `down` argument overrides the current down state, if not None.

        When `track_angle` is true, movement tracks concurrent updates to the
        Turtle's angle, potentially resulting in non-linear paths. Otherwise,
        movement follows a straight line, set by the starting Turtle's angle.

        The `speed`, `easing`, `fps`, and `update` values are passed to the
        underlying Sprite's animated movement operation.
        """
        self._line_id = None
        self._line_coords = list(self._sprite.anchor)
        with self._down_override(down):
            await self._sprite.async_forward(
                delta,
                callback=self._async_draw_line if self.down else None,
                track_angle=track_angle,
                speed=speed,
                easing=easing,
                fps=fps,
                update=update,
            )


    async def async_move(self, dx, dy, *, down=None, speed=None, easing=None,
                         fps=None, update=None):
        """
        Animated move of the Turtle by the given relative `dx` and `dy` values.

        The `down` argument overrides the current down state, if not None.

        The `speed`, `easing`, `fps`, and `update` values are passed to
        the underlying Sprite's animated movement operation.
        """
        self._line_id = None
        self._line_coords = list(self._sprite.anchor)
        with self._down_override(down):
            await self._sprite.async_move(
                dx, dy,
                callback=self._async_draw_line if self.down else None,
                speed=speed,
                easing=easing,
                fps=fps,
                update=update,
            )


    async def async_move_to(self, x, y, *, down=None, speed=None, easing=None,
                            fps=None, update=None):
        """
        Animated move of the Turtle to the given absolute `x` and `y` position.

        The `down` argument overrides the current down state, if not None.

        The `speed`, `easing`, `fps`, and `update` values are passed to
        the underlying Sprite's animated movement operation.
        """
        self._line_id = None
        self._line_coords = list(self._sprite.anchor)
        with self._down_override(down):
            await self._sprite.async_move_to(
                x, y,
                callback=self._async_draw_line if self.down else None,
                speed=speed,
                easing=easing,
                fps=fps,
                update=update,
            )


    async def async_left(self, angle, *, speed=None, easing=None, fps=None,
                         update=None):
        """
        Animated, counterclockwise rotation of the Turtle, by `angle` degrees.

        The `speed`, `easing`, `fps`, and `update` values are passed to the
        underlying Sprite's animated movement operation.
        """
        await self._sprite.async_rotate(
            angle,
            speed=speed,
            easing=easing,
            fps=fps,
            update=update,
        )


    async def async_right(self, angle, *, speed=None, easing=None, fps=None,
                          update=None):
        """
        Animated, clockwise rotation of the Turtle, by `angle` degrees.

        The `speed`, `easing`, `fps`, and `update` values are passed to the
        underlying Sprite's animated movement operation.
        """
        await self._sprite.async_rotate(
            -angle,
            speed=speed,
            easing=easing,
            fps=fps,
            update=update,
        )


    # ------------------------------------------------------------------------
    # Sync animated movement and rotation methods.
    #
    # The synchronous versions of the async animated movement and rotation
    # methods are automatically generated by the code in the `syncer` module.
    #
    # The `name_mapper` function is defined exclusively for this purpuse,
    # being deleted after the fact, in order not to pollute the class attrs.

    def name_mapper(name):
        # Only maps names starting with `_async_` or `async_`.
        if name.startswith('_async_'):
            return '_' + name[2:]
        if name.startswith('async_'):
            return name[1:]
        return name

    _sync_draw_line = syncer.create_sync_func(_async_draw_line, name_mapper)
    sync_forward = syncer.create_sync_func(async_forward, name_mapper)
    sync_move = syncer.create_sync_func(async_move, name_mapper)
    sync_move_to = syncer.create_sync_func(async_move_to, name_mapper)
    sync_left = syncer.create_sync_func(async_left, name_mapper)
    sync_right = syncer.create_sync_func(async_right, name_mapper)

    del name_mapper
