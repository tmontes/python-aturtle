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
    """
    Sprite animation error.
    """



class _ConcurrentAnimationContexts:
    """
    Provides two concurrent animation controlling context managers:
    one for relative animation, and another for absolute animation.

    Supports concurrent relative animations and prevents any concurrency
    when absolute animations are active.
    """
    def __init__(self, name):

        self._name = name
        self._relative_count = 0
        self._absolute_count = 0


    @contextlib.contextmanager
    def relative(self):
        """
        Tracks running relative animations. Raises `AnimationError` on enter,
        if absolute animations are active.
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
        Tracks running absolute animations. Raises `AnimationError` on enter,
        if any animations are active.
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
    Sprite base class.
    """

    def __init__(self, canvas, shape, *, anchor=(0, 0), angle=0, speed=360,
                 m_speed=None, r_speed=None, easing=None, m_easing=None,
                 r_easing=None, m_callback=None, r_callback=None, fps=80,
                 update=False):
        """
        Initialize a Sprite with the given `shape` and place it on the output
        `canvas` at the given `x`, `y` coordinates, rotated `angle` degrees.

        Sprite moves at `m_speed` canvas units per second, and rotates at
        `r_speed` degrees per second; if None they default to `speed`.

        Movement speed is changed by the `m_easing` callable, if passed, and
        rotation speed is changed by the `r_easing` callable; if None, they
        default to the `easing` callable.

        If set, `m_callback` is called once per frame with (progress, anchor)
        positional arguments, where progress is a number that goes from 0 to 1
        througout the animation, and anchor is an (x, y) tuple with the Sprite's
        position at the time. If set, `r_callback` is called once per frame with
        (progress, angle) positional arguments, where progress is as above, and
        angle is the Sprite's angle at the time.

        Movement and rotation animations generate an aproximation of `fps`
        frames per second.

        When `update` is true, the output canvas is updated automatically with
        on movement or rotation.
        """
        self._canvas = canvas
        self._id = None

        self._shape = shape
        self._anchor = anchor
        self._angle = angle

        self._m_speed = m_speed if m_speed is not None else speed
        self._r_speed = r_speed if r_speed is not None else speed
        self._m_easing = m_easing if m_easing is not None else easing
        self._r_easing = r_easing if r_easing is not None else easing
        self._m_callback = m_callback
        self._r_callback = r_callback
        self._fps = fps
        self._update = update

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


    def move(self, dx=0, dy=0, *, update=None):
        """
        Move the Sprite by the given relative `dx` and `dy` values.
        The `update` argument overrides the initialized value.
        """
        sprite_x, sprite_y = self._anchor
        self._anchor = (sprite_x + dx, sprite_y + dy)
        self._canvas.move(self._id, dx, dy)

        update = self._update if update is None else update
        if update:
            self.update()


    def move_to(self, x=0, y=0, *, update=None):
        """
        Move the Sprite to the given absolute `x`, `y` position.
        The `update` argument overrides the initialized value.
        """
        sprite_x, sprite_y = self._anchor
        self.move(x - sprite_x, y - sprite_y, update=update)


    async def async_move(self, dx, dy, *, speed=None, easing=None, callback=None,
                         fps=None, update=None):
        """
        Move the Sprite by the given relative `dx` and `dy` values.

        The `speed`, `easing`, `callback`, `fps`, and `update` arguments over-
        ride the initialized values.
        """
        with self._movement.relative(), contextlib.suppress(asyncio.CancelledError):

            speed = self._r_speed if speed is None else speed
            update = self._update if update is None else update
            easing = self._m_easing if easing is None else easing
            callback = self._m_callback if callback is None else callback
            fps = self._fps if fps is None else fps

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
                    await callback(eased_progress, self._anchor)
                await asyncio.sleep(frame_seconds)
                prev_eased_progress = eased_progress


    async def async_move_to(self, x, y, *, speed=None, easing=None, callback=None,
                            fps=None, update=None):
        """
        Move the Sprite to the given absolute (`x`, `y`) position.

        The `speed`, `easing`, `callback`, `fps`, and `update` arguments over-
        ride the initialized values.
        """
        with self._movement.absolute(), contextlib.suppress(asyncio.CancelledError):

            speed = self._r_speed if speed is None else speed
            update = self._update if update is None else update
            easing = self._m_easing if easing is None else easing
            callback = self._m_callback if callback is None else callback
            fps = self._fps if fps is None else fps

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
                    await callback(eased_progress, self._anchor)
                await asyncio.sleep(frame_seconds)


    def rotate(self, angle=0, *, around=None, update=None):
        """
        Rotate the Sprite anchor by `angle` degrees. If `around` is None, the
        anchor is left unchanged. Otherwise, rotate it about `around`, assumed
        to be a (cx, cy) two-tuple defining the center of rotation.
        The `update` argument overrides the initialized value.
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

        update = self._update if update is None else update
        if update:
            self.update()


    def rotate_to(self, angle=0, around=None, update=None):
        """
        Rotate the Sprite anchor to `angle` degrees, with 0 being the underlying
        shape's original orientation. If `anchor` is None, the anchor is left
        unchanged. Otherwise, it is rotated around it, assumed to be a (cx, cy)
        two-tuple defining the center of rotation.
        The `update` argument overrides the initialized value.
        """
        self.rotate(angle-self._angle, around=around, update=update)


    async def async_rotate(self, dangle, *, around=None, speed=None, easing=None,
                           callback=None, fps=None, update=None):
        """
        Rotate the Sprite anchor by `angle` degrees. If `around` is None, the
        anchor is left unchanged. Otherwise, rotate it about `around`, assumed
        to be a (cx, cy) two-tuple defining the center of rotation.

        The `speed`, `easing`, `callback`, `fps`, and `update` arguments over-
        ride the initialized values. If `speed` is None, there's no animation.
        """
        with self._rotation.relative(), contextlib.suppress(asyncio.CancelledError):

            speed = self._r_speed if speed is None else speed
            update = self._update if update is None else update
            easing = self._r_easing if easing is None else easing
            callback = self._r_callback if callback is None else callback
            fps = self._fps if fps is None else fps

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
                    await callback(eased_progress, self._angle)
                await asyncio.sleep(frame_seconds)
                prev_eased_progress = eased_progress


    async def async_rotate_to(self, angle, *, around=None, speed=None, easing=None,
                              callback=None, fps=None, update=None):
        """
        Rotate the Sprite anchor to `angle` degrees, with 0 being the underlying
        shape's original orientation. If `anchor` is None, the anchor is left
        unchanged. Otherwise, it is rotated around it, assumed to be a (cx, cy)
        two-tuple defining the center of rotation.

        The `speed`, `easing`, `callback`, `fps`, and `update` arguments over-
        ride the initialized values. If `speed` is None, there's no animation.
        """
        with self._rotation.absolute(), contextlib.suppress(asyncio.CancelledError):

            speed = self._r_speed if speed is None else speed
            update = self._update if update is None else update
            easing = self._r_easing if easing is None else easing
            callback = self._r_callback if callback is None else callback
            fps = self._fps if fps is None else fps

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
                    await callback(eased_progress, self._angle)
                await asyncio.sleep(frame_seconds)


    def update(self):
        """
        Update the output canvas to reflect the current Sprite state.
        """
        self._canvas.update()


    def delete(self):
        """
        Remove the Sprite from the output canvas, getting ready for disposal.
        """
        if self._id:
            self._canvas.delete(self._id)
            self._id = None
