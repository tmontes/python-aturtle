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

        self._down = bool(down)
        self.line_color = line_color
        self.line_width = line_width

        self._line_id = None
        self._line_start = None
        self._lines = []


    def up(self):
        """
        Raises the turtle from the canvas. No lines are drawn as it moves.
        """
        self._down = False


    def down(self):
        """
        Lowers the turtle onto the canvas. Lines are drawn as it moves.
        """
        self._down = True


    def isdown(self):
        """
        True if turtle movements draw lines. False otherwise.
        """
        return self._down


    async def _async_draw_line(self, _progress, anchor):
        """
        Sprite movement callback to handle line drawing.
        """
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


    async def async_forward(self, distance, *, speed=None, easing=None,
                            fps=None, update=None):
        """
        Animated move of the Turtle forward by `distance`, towards the
        direction set by its angle. Negative values move the Turtle in
        the opposite direction.

        The `speed`, `easing`, `fps`, and `update` values are passed to
        the underlying Sprite's animated movement operation.
        """
        self._line_id = None
        self._line_start = self._sprite.anchor
        await self._sprite.async_forward(
            distance,
            callback=self._async_draw_line if self._down else None,
            speed=speed,
            easing=easing,
            fps=fps,
            update=update,
        )


    async def async_backward(self, distance, *, speed=None, easing=None,
                             fps=None, update=None):
        """
        Animated move of the Turtle backward by `distance`, away from the
        direction set by its angle. Negative values move the Turtle in
        the opposite direction.

        The `speed`, `easing`, `fps`, and `update` values are passed to
        the underlying Sprite's animated movement operation.
        """
        await self.async_forward(
            -distance,
            speed=speed,
            easing=easing,
            fps=fps,
            update=update,
        )


    async def async_move(self, dx, dy, *, speed=None, easing=None, fps=None,
                         update=None):
        """
        Animated move of the Turtle by the given relative `dx` and `dy` values.

        The `speed`, `easing`, `fps`, and `update` values are passed to
        the underlying Sprite's animated movement operation.
        """
        self._line_id = None
        self._line_start = self._sprite.anchor
        await self._sprite.async_move(
            dx, dy,
            callback=self._async_draw_line if self._down else None,
            speed=speed,
            easing=easing,
            fps=fps,
            update=update,
        )


    async def async_move_to(self, x, y, *, speed=None, easing=None, fps=None,
                            update=None):
        """
        Animated move of the Turtle to the given absolute `x` and `y` position.

        The `speed`, `easing`, `fps`, and `update` values are passed to
        the underlying Sprite's animated movement operation.
        """
        self._line_id = None
        self._line_start = self._sprite.anchor
        await self._sprite.async_move_to(
            x, y,
            callback=self._async_draw_line if self._down else None,
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
            -angle,
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
            angle,
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
    sync_backward = syncer.create_sync_func(async_backward, name_mapper)
    sync_move = syncer.create_sync_func(async_move, name_mapper)
    sync_move_to = syncer.create_sync_func(async_move_to, name_mapper)
    sync_left = syncer.create_sync_func(async_left, name_mapper)
    sync_right = syncer.create_sync_func(async_right, name_mapper)

    del name_mapper
