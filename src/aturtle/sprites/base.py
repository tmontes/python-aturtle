# ----------------------------------------------------------------------------
# Python A-Turtle
# ----------------------------------------------------------------------------
# Copyright (c) Tiago Montes.
# See LICENSE for details.
# ----------------------------------------------------------------------------

import asyncio
import contextlib
import math



class AnimationError(Exception):
    pass



class _ConcurrentAnimationContexts:
    """
    Provides two concurrent animation controlling context managers:
    one for relative animation, and another for absolute animation.

    Supporting concurrent / cumulative relative animations, while preventing
    any concurrency when absolute based animations are active.
    """
    def __init__(self, name):

        self._name = name
        self._relative_count = 0
        self._absolute_count = 0


    @contextlib.contextmanager
    def relative(self):
        """
        Raises `AnimationError` when entering if absolute animations are active.
        """
        if self._absolute_count:
            raise AnimationError(f'{self._absolute_count} active absolute {self._name}')

        self._relative_count += 1
        try:
            yield
        finally:
            self._relative_count -= 1


    @contextlib.contextmanager
    def absolute(self):
        """
        Raises `AnimationError` when entering if any animations are active.
        """
        if self._relative_count:
            raise AnimationError(f'{self._relative_count} active relative {self._name}')
        if self._absolute_count:
            raise AnimationError(f'{self._absolute_count} active absolute {self._name}')

        self._absolute_count += 1
        try:
            yield
        finally:
            self._absolute_count -= 1



class Sprite:

    """
    Base class.
    """

    def __init__(self, canvas, shape, *, anchor=(0, 0), angle=0):
        """
        Initialize a Sprite with the given `shape` and place it on the output
        `canvas` at the given `x`, `y` coordinates, rotated `angle` degrees.
        """
        self._canvas = canvas
        self._id = None

        self._shape = shape
        self._anchor = anchor
        self._angle = angle

        self._movement = _ConcurrentAnimationContexts('moves')
        self._rotation = _ConcurrentAnimationContexts('rotates')


    @property
    def anchor(self):
        """
        The Sprite's anchor position in the canvas, as an (x, y) tuple.
        """
        return self._anchor


    @property
    def angle(self):
        """
        The Sprite's rotation angle, in degrees.
        """
        return self._angle


    def move(self, dx=0, dy=0, *, update=False):
        """
        Move the Sprite by the given relative `dx` and `dy` values.
        Update the output if `update` is true.
        """
        sprite_x, sprite_y = self._anchor
        self._anchor = (sprite_x + dx, sprite_y + dy)
        self._canvas.move(self._id, dx, dy)
        if update:
            self.update()


    def move_to(self, x=0, y=0, *, update=False):
        """
        Move the Sprite to the given absolute (`x`, `y`) position.
        Update the output if `update` is true.
        """
        sprite_x, sprite_y = self._anchor
        self.move(x - sprite_x, y - sprite_y, update=update)


    async def a_move(self, dx, dy, *, speed=100, fps=50, easing=None,
                     callback=None, update=False):
        """
        `speed` in units per second
        `fps` how many updates/moves per second
        `easing` callable mapping time to progress, both in the [0, 1] range
        `callback` called once per frame, with current (progress, anchor).
        """
        with self._movement.relative(), contextlib.suppress(asyncio.CancelledError):

            if speed is None:
                self.move(dx, dy, update=update)
                return

            distance = (dx ** 2 + dy ** 2) ** 0.5
            total_seconds = distance / speed
            total_frames = int(total_seconds * fps)
            frame_seconds = 1 / fps

            frame_dx = dx / total_frames
            frame_dy = dy / total_frames

            prev_eased_progress = 0
            for frame in range(1, total_frames+1):
                progress = frame / total_frames
                eased_progress = easing(progress) if easing else progress
                eased_delta = (eased_progress - prev_eased_progress) * total_frames
                self.move(frame_dx * eased_delta, frame_dy * eased_delta, update=update)
                if callback:
                    callback(eased_progress, self._anchor)
                await asyncio.sleep(frame_seconds)
                prev_eased_progress = eased_progress


    async def a_move_to(self, x, y, *, speed=100, fps=50, easing=None,
                        callback=None, update=False):
        """
        `speed` in units per second
        `fps` how many updates/moves per second
        `easing` callable mapping time to progress, both in the [0, 1] range
        """
        with self._movement.absolute(), contextlib.suppress(asyncio.CancelledError):

            if speed is None:
                self.move_to(x, y, update=update)
                return

            start_x, start_y = self._anchor
            dx = x - start_x
            dy = y - start_y

            distance = (dx ** 2 + dy ** 2) ** 0.5
            total_seconds = distance / speed
            total_frames = int(total_seconds * fps)
            frame_seconds = 1 / fps

            for frame in range(1, total_frames+1):
                progress = frame / total_frames
                eased_progress = easing(progress) if easing else progress
                frame_x = start_x + dx * eased_progress
                frame_y = start_y + dy * eased_progress
                self.move_to(frame_x, frame_y, update=update)
                if callback:
                    callback(eased_progress, self._anchor)
                await asyncio.sleep(frame_seconds)


    def rotate(self, angle=0, *, around=None, update=False):
        """
        Rotate the Sprite anchor by `angle` degrees. If `around` is None, the
        anchor is left unchanged. Otherwise, rotate it about `around`, assumed
        to be a (cx, cy) two-tuple defining the center of rotation.
        Update the output if `update` is true.
        """
        self._angle = (self._angle + angle) % 360
        angle_rad = angle * math.pi / 180.0
        if around:
            sprite_x, sprite_y = self._anchor
            cx, cy = around
            sprite_x -= cx
            sprite_y -= cy
            sin_theta = math.sin(angle_rad)
            cos_theta = math.cos(angle_rad)
            new_x = sprite_x * cos_theta - sprite_y * sin_theta + cx
            new_y = sprite_x * sin_theta + sprite_y * cos_theta + cy
            self._anchor = (new_x, new_y)
        if update:
            self.update()


    def rotate_to(self, angle=0, around=None, update=False):
        """
        Rotate the Sprite anchor to `angle` degrees, with 0 being the
        underlying shape's original orientation. If `anchor` is None,
        the anchor is left unchanged. Otherwise, it is rotated around
        it, assumed to be a (cx, cy) two-tuple defining the center of
        rotation.
        Update the output if `update` is true.
        """
        self.rotate(angle-self._angle, around=around, update=update)


    async def a_rotate(self, dangle, *, around=None, speed=360, fps=50,
                       easing=None, callback=None, update=False):
        """
        `speed` in degrees per second
        `fps` how many updates/rotations per second
        `easing` callable mapping time to progress, both in the [0, 1] range
        `callback` called once per frame, with current (progress, angle).
        """
        with self._rotation.relative(), contextlib.suppress(asyncio.CancelledError):

            if speed is None:
                self.rotate(dangle, around=around, update=update)
                return

            total_seconds = abs(dangle / speed)
            total_frames = int(total_seconds * fps)
            frame_seconds = 1 / fps

            frame_dangle = dangle / total_frames

            prev_eased_progress = 0
            for frame in range(1, total_frames+1):
                progress = frame / total_frames
                eased_progress = easing(progress) if easing else progress
                eased_delta = (eased_progress - prev_eased_progress) * total_frames
                self.rotate(frame_dangle * eased_delta, around=around, update=update)
                if callback:
                    callback(eased_progress, self._angle)
                await asyncio.sleep(frame_seconds)
                prev_eased_progress = eased_progress


    async def a_rotate_to(self, angle, *, around=None, speed=360, fps=50,
                          easing=None, callback=None, update=False):
        """
        `speed` in degrees per second
        `fps` how many updates/rotations per second
        `easing` callable mapping time to progress, both in the [0, 1] range
        """
        with self._rotation.absolute(), contextlib.suppress(asyncio.CancelledError):

            if speed is None:
                self.rotate_to(angle, around=around, update=update)
                return

            start_angle = self._angle
            dangle = (angle - start_angle) % 360
            if dangle > 180:
                dangle = dangle - 360

            total_seconds = abs(dangle / speed)
            total_frames = int(total_seconds * fps)
            frame_seconds = 1 / fps

            for frame in range(1, total_frames+1):
                progress = frame / total_frames
                eased_progress = easing(progress) if easing else progress
                frame_angle = start_angle + dangle * eased_progress
                self.rotate_to(frame_angle, around=around, update=update)
                if callback:
                    callback(eased_progress, self._angle)
                await asyncio.sleep(frame_seconds)


    def update(self):
        """
        Update the the output by redrawing pending movements or rotations.
        """
        self._canvas.update()


    def delete(self):
        """
        Remove the Sprite from the output, getting ready for object deletion.
        """
        if self._id:
            self._canvas.delete(self._id)
            self._id = None
