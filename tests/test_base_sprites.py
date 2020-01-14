# ----------------------------------------------------------------------------
# Python A-Turtle
# ----------------------------------------------------------------------------
# Copyright (c) Tiago Montes.
# See LICENSE for details.
# ----------------------------------------------------------------------------

import collections
import contextlib
from unittest import mock

from aturtle.sprites import base

from . import base as test_base
from . import fake_tkinter
from . import fake_asyncio



class TestDefaultSprite(test_base.TestCase):

    def setUp(self):

        self.canvas = fake_tkinter.FakeCanvas()


    def test_create(self):

        _sprite = base.Sprite(canvas=self.canvas, shape=None)


    def test_default_anchor(self):

        sprite = base.Sprite(canvas=self.canvas, shape=None)
        self.assert_almost_equal_anchor(sprite.anchor, (0, 0), places=1)


    def test_default_angle(self):

        sprite = base.Sprite(canvas=self.canvas, shape=None)
        self.assertAlmostEqual(sprite.angle, 0, places=1)


    def test_direct_move_moves_anchor(self):

        sprite = base.Sprite(canvas=self.canvas, shape=None)
        sprite.direct_move(42, 24)
        self.assert_almost_equal_anchor(sprite.anchor, (42, 24), places=1)


    def test_direct_move_moves_anchor_relative(self):

        sprite = base.Sprite(canvas=self.canvas, shape=None)
        sprite.direct_move(42, 0)
        sprite.direct_move(0, 24)
        self.assert_almost_equal_anchor(sprite.anchor, (42, 24), places=1)


    def test_direct_move_does_not_change_angle(self):

        sprite = base.Sprite(canvas=self.canvas, shape=None)
        sprite.direct_move(42, 24)
        self.assertAlmostEqual(sprite.angle, 0, places=1)


    def test_direct_move_to_moves_anchor(self):

        sprite = base.Sprite(canvas=self.canvas, shape=None)
        sprite.direct_move_to(42, 24)
        self.assert_almost_equal_anchor(sprite.anchor, (42, 24), places=1)


    def test_direct_move_to_moves_anchor_absolute(self):

        sprite = base.Sprite(canvas=self.canvas, shape=None)
        sprite.direct_move_to(42, 0)
        sprite.direct_move_to(0, 24)
        self.assert_almost_equal_anchor(sprite.anchor, (0, 24), places=1)


    def test_direct_move_to_does_not_change_angle(self):

        sprite = base.Sprite(canvas=self.canvas, shape=None)
        sprite.direct_move_to(42, 24)
        self.assertAlmostEqual(sprite.angle, 0, places=1)


    def test_direct_rotate_does_not_move_anchor(self):

        sprite = base.Sprite(canvas=self.canvas, shape=None)
        sprite.direct_rotate(90)
        self.assert_almost_equal_anchor(sprite.anchor, (0, 0), places=1)


    def test_direct_rotate_around_moves_anchor(self):

        sprite = base.Sprite(canvas=self.canvas, shape=None)
        sprite.direct_rotate(180, around=(1, 1))
        self.assert_almost_equal_anchor(sprite.anchor, (2, 2), places=1)


    def test_direct_rotate_around_moves_anchor_relative(self):

        sprite = base.Sprite(canvas=self.canvas, shape=None)
        sprite.direct_rotate(90, around=(1, 1))
        sprite.direct_rotate(90, around=(1, 1))
        self.assert_almost_equal_anchor(sprite.anchor, (2, 2), places=1)


    def test_direct_rotate_changes_angle(self):

        sprite = base.Sprite(canvas=self.canvas, shape=None)
        sprite.direct_rotate(90)
        self.assertAlmostEqual(sprite.angle, 90, places=1)


    def test_direct_rotate_changes_angle_relative(self):

        sprite = base.Sprite(canvas=self.canvas, shape=None)
        sprite.direct_rotate(45)
        sprite.direct_rotate(45)
        self.assertAlmostEqual(sprite.angle, 90, places=1)


    def test_direct_rotate_around_changes_angle(self):

        sprite = base.Sprite(canvas=self.canvas, shape=None)
        sprite.direct_rotate(90, around=(1, 1))
        self.assertAlmostEqual(sprite.angle, 90, places=1)


    def test_direct_rotate_to_does_not_move_anchor(self):

        sprite = base.Sprite(canvas=self.canvas, shape=None)
        sprite.direct_rotate_to(90)
        self.assert_almost_equal_anchor(sprite.anchor, (0, 0), places=1)


    def test_direct_rotate_to_around_moves_anchor(self):

        sprite = base.Sprite(canvas=self.canvas, shape=None)
        sprite.direct_rotate_to(180, around=(1, 1))
        self.assert_almost_equal_anchor(sprite.anchor, (2, 2), places=1)


    def test_direct_rotate_to_around_moves_anchor_absolute(self):

        sprite = base.Sprite(canvas=self.canvas, shape=None)
        sprite.direct_rotate_to(90, around=(1, 1))
        sprite.direct_rotate_to(180, around=(1, 1))
        self.assert_almost_equal_anchor(sprite.anchor, (2, 2), places=1)


    def test_direct_rotate_to_changes_angle(self):

        sprite = base.Sprite(canvas=self.canvas, shape=None)
        sprite.direct_rotate_to(90)
        self.assertAlmostEqual(sprite.angle, 90, places=1)


    def test_direct_rotate_to_changes_angle_absolute(self):

        sprite = base.Sprite(canvas=self.canvas, shape=None)
        sprite.direct_rotate_to(20)
        sprite.direct_rotate_to(90)
        self.assertAlmostEqual(sprite.angle, 90, places=1)


    def test_direct_rotate_to_around_changes_angle(self):

        sprite = base.Sprite(canvas=self.canvas, shape=None)
        sprite.direct_rotate_to(90, around=(1, 1))
        self.assertAlmostEqual(sprite.angle, 90, places=1)


    def test_direct_move_with_no_update_does_not_call_canvas_update(self):

        sprite = base.Sprite(canvas=self.canvas, shape=None)
        sprite.direct_move(42, 24)
        self.canvas.update.assert_not_called()


    def test_direct_move_with_update_calls_canvas_update(self):

        sprite = base.Sprite(canvas=self.canvas, shape=None)
        sprite.direct_move(42, 24, update=True)
        self.canvas.update.assert_called_once_with()


    def test_direct_move_to_with_no_update_does_not_call_canvas_update(self):

        sprite = base.Sprite(canvas=self.canvas, shape=None)
        sprite.direct_move_to(42, 24)
        self.canvas.update.assert_not_called()


    def test_direct_move_to_with_update_calls_canvas_update(self):

        sprite = base.Sprite(canvas=self.canvas, shape=None)
        sprite.direct_move_to(42, 24, update=True)
        self.canvas.update.assert_called_once_with()


    def test_direct_rotate_with_no_update_does_not_call_canvas_update(self):

        sprite = base.Sprite(canvas=self.canvas, shape=None)
        sprite.direct_rotate(42)
        self.canvas.update.assert_not_called()


    def test_direct_rotate_with_update_calls_canvas_update(self):

        sprite = base.Sprite(canvas=self.canvas, shape=None)
        sprite.direct_rotate(42, update=True)
        self.canvas.update.assert_called_once_with()


    def test_direct_rotate_to_with_no_update_does_not_call_canvas_update(self):

        sprite = base.Sprite(canvas=self.canvas, shape=None)
        sprite.direct_rotate_to(42)
        self.canvas.update.assert_not_called()


    def test_direct_rotate_to_with_update_calls_canvas_update(self):

        sprite = base.Sprite(canvas=self.canvas, shape=None)
        sprite.direct_rotate_to(42, update=True)
        self.canvas.update.assert_called_once_with()



class TestNonDefaultSprite(test_base.TestCase):

    def setUp(self):

        self.canvas = fake_tkinter.FakeCanvas()
        self.sprite = base.Sprite(
            canvas=self.canvas,
            shape=None,
            anchor=(42, 24),
            angle=42,
        )


    def test_anchor(self):

        self.assert_almost_equal_anchor(self.sprite.anchor, (42, 24), places=1)


    def test_angle(self):

        self.assertAlmostEqual(self.sprite.angle, 42, places=1)


    def test_direct_move_moves_anchor(self):

        self.sprite.direct_move(-42, -24)
        self.assert_almost_equal_anchor(self.sprite.anchor, (0, 0), places=1)


    def test_direct_move_moves_anchor_relative(self):

        self.sprite.direct_move(-42, 0)
        self.sprite.direct_move(0, -24)
        self.assert_almost_equal_anchor(self.sprite.anchor, (0, 0), places=1)


    def test_direct_move_does_not_change_angle(self):

        self.sprite.direct_move(42, 24)
        self.assertAlmostEqual(self.sprite.angle, 42, places=1)


    def test_direct_move_to_moves_anchor(self):

        self.sprite.direct_move_to(20, 10)
        self.assert_almost_equal_anchor(self.sprite.anchor, (20, 10), places=1)


    def test_direct_move_to_moves_anchor_absolute(self):

        self.sprite.direct_move_to(42, 0)
        self.sprite.direct_move_to(0, 24)
        self.assert_almost_equal_anchor(self.sprite.anchor, (0, 24), places=1)


    def test_direct_move_to_does_not_change_angle(self):

        self.sprite.direct_move_to(42, 24)
        self.assertAlmostEqual(self.sprite.angle, 42, places=1)


    def test_direct_rotate_does_not_move_anchor(self):

        self.sprite.direct_rotate(90)
        self.assert_almost_equal_anchor(self.sprite.anchor, (42, 24), places=1)


    def test_direct_rotate_around_moves_anchor(self):

        self.sprite.direct_rotate(180, around=(0, 0))
        self.assert_almost_equal_anchor(self.sprite.anchor, (-42, -24), places=1)


    def test_direct_rotate_around_moves_anchor_relative(self):

        self.sprite.direct_rotate(90, around=(0, 0))
        self.sprite.direct_rotate(90, around=(0, 0))
        self.assert_almost_equal_anchor(self.sprite.anchor, (-42, -24), places=1)


    def test_direct_rotate_changes_angle(self):

        self.sprite.direct_rotate(-42)
        self.assertAlmostEqual(self.sprite.angle, 0, places=1)


    def test_direct_rotate_changes_angle_relative(self):

        self.sprite.direct_rotate(-40)
        self.sprite.direct_rotate(-2)
        self.assertAlmostEqual(self.sprite.angle, 0, places=1)


    def test_direct_rotate_around_changes_angle(self):

        self.sprite.direct_rotate(-42, around=(1, 1))
        self.assertAlmostEqual(self.sprite.angle, 0, places=1)


    def test_direct_rotate_to_does_not_move_anchor(self):

        self.sprite.direct_rotate_to(90)
        self.assert_almost_equal_anchor(self.sprite.anchor, (42, 24), places=1)


    def test_direct_rotate_to_around_moves_anchor(self):

        self.sprite.direct_rotate_to(42+180, around=(0, 0))
        self.assert_almost_equal_anchor(self.sprite.anchor, (-42, -24), places=1)


    def test_direct_rotate_to_around_moves_anchor_absolute(self):

        self.sprite.direct_rotate_to(90, around=(0, 0))
        self.sprite.direct_rotate_to(42+180, around=(0, 0))
        self.assert_almost_equal_anchor(self.sprite.anchor, (-42, -24), places=1)


    def test_direct_rotate_to_changes_angle(self):

        self.sprite.direct_rotate_to(90)
        self.assertAlmostEqual(self.sprite.angle, 90, places=1)


    def test_direct_rotate_to_changes_angle_absolute(self):

        self.sprite.direct_rotate_to(20)
        self.sprite.direct_rotate_to(90)
        self.assertAlmostEqual(self.sprite.angle, 90, places=1)


    def test_direct_rotate_to_around_changes_angle(self):

        self.sprite.direct_rotate_to(90, around=(1, 1))
        self.assertAlmostEqual(self.sprite.angle, 90, places=1)


    def test_direct_move_with_no_update_does_not_call_canvas_update(self):

        self.sprite.direct_move(42, 24)
        self.canvas.update.assert_not_called()


    def test_direct_move_with_update_calls_canvas_update(self):

        self.sprite.direct_move(42, 24, update=True)
        self.canvas.update.assert_called_once_with()


    def test_direct_move_to_with_no_update_does_not_call_canvas_update(self):

        self.sprite.direct_move_to(42, 24)
        self.canvas.update.assert_not_called()


    def test_direct_move_to_with_update_calls_canvas_update(self):

        self.sprite.direct_move_to(42, 24, update=True)
        self.canvas.update.assert_called_once_with()


    def test_direct_rotate_with_no_update_does_not_call_canvas_update(self):

        self.sprite.direct_rotate(42)
        self.canvas.update.assert_not_called()


    def test_direct_rotate_with_update_calls_canvas_update(self):

        self.sprite.direct_rotate(42, update=True)
        self.canvas.update.assert_called_once_with()


    def test_direct_rotate_to_with_no_update_does_not_call_canvas_update(self):

        self.sprite.direct_rotate_to(42)
        self.canvas.update.assert_not_called()


    def test_direct_rotate_to_with_update_calls_canvas_update(self):

        self.sprite.direct_rotate_to(42, update=True)
        self.canvas.update.assert_called_once_with()



class AsyncAnimationBase(test_base.TestCase):

    def setUp(self):

        self.canvas = fake_tkinter.FakeCanvas()

        self.asyncio = fake_asyncio.FakeAsyncio()
        self._exit_stack = contextlib.ExitStack()
        self._exit_stack.enter_context(
            mock.patch('aturtle.sprites.base.asyncio', self.asyncio)
        )


    def tearDown(self):

        self._exit_stack.close()


    def _run_coroutines(self, *coros):

        ready = collections.deque(coros)
        while ready:
            coro = ready.popleft()
            try:
                coro.send(None)
            except StopIteration:
                pass
            else:
                ready.append(coro)



class TestAsyncMoveAnimation(AsyncAnimationBase):

    def setUp(self):

        super().setUp()
        self.sprite = base.Sprite(canvas=self.canvas, shape=None, anchor=(0, 0))


    def test_async_move_with_speed_moves_anchor(self):

        coro = self.sprite.async_move(40, 30, speed=50, fps=10)
        self._run_coroutines(coro)

        self.assert_almost_equal_anchor(self.sprite.anchor, (40, 30), places=1)


    def test_async_move_with_speed_calls_canvas_move_and_asyncio_sleep(self):

        coro = self.sprite.async_move(40, 30, speed=50, fps=10)
        self._run_coroutines(coro)

        # Given that the move distance is 50 and the speed is 50, animation
        # duration is 1 second. At 10 fps, 10 frames must be generated: each
        # with a call to canvas.move of 1/10th the distance and an await of
        # asyncio.sleep of 1/10th the duration.

        canvas_move_calls = self.canvas.move.call_args_list
        self.assertEqual(len(canvas_move_calls), 10, 'canvas.move call count')
        for call in canvas_move_calls:
            _shape_id, dx, dy = call.args
            self.assertAlmostEqual(dx, 4, places=1)
            self.assertAlmostEqual(dy, 3, places=1)

        asyncio_sleep_call_args = self.asyncio.sleep_call_args
        self.assertEqual(len(asyncio_sleep_call_args), 10, 'asyncio.sleep await count')
        for sleep_duration in asyncio_sleep_call_args:
            self.assertAlmostEqual(sleep_duration, 0.1, places=3)

        # TODO: A more correct test would check that canvas.move calls and
        # asyncio.sleep awaits are called in alternating turns.


    def test_async_move_with_speed_and_easing_progresses_non_linearly(self):

        def easing(progress):
            return 0 if progress < 0.5 else 1

        coro = self.sprite.async_move(40, 30, speed=50, fps=10, easing=easing)
        self._run_coroutines(coro)

        # canvas.move should have been called 10 times:
        # - First 4 with no movement.
        # - 5th with the whole movement.
        # - Remaining with no movement.

        canvas_move_calls = self.canvas.move.call_args_list
        self.assertEqual(len(canvas_move_calls), 10, 'canvas.move call count')
        for call in canvas_move_calls[:4]:
            _shape_id, dx, dy = call.args
            self.assertAlmostEqual(dx, 0, places=1)
            self.assertAlmostEqual(dy, 0, places=1)

        _shape_id, dx, dy = canvas_move_calls[4].args
        self.assertAlmostEqual(dx, 40, places=1)
        self.assertAlmostEqual(dy, 30, places=1)

        for call in canvas_move_calls[5:]:
            _shape_id, dx, dy = call.args
            self.assertAlmostEqual(dx, 0, places=1)
            self.assertAlmostEqual(dy, 0, places=1)


    def test_async_move_with_speed_calls_callback(self):

        data = []
        async def cb(*args):
            data.append(args)

        coro = self.sprite.async_move(40, 30, speed=50, fps=10, callback=cb)
        self._run_coroutines(coro)

        # Data should have 10 (progress, (x, y)) tuples:
        self.assertEqual(len(data), 10, 'callback count')
        for i, (progress, (x, y)) in enumerate(data, start=1):
            self.assertAlmostEqual(progress, i/10, places=3)
            self.assertAlmostEqual(x, 40*progress, places=1)
            self.assertAlmostEqual(y, 30*progress, places=1)


    def test_async_move_with_high_speed_and_nearly_zero_frames_works(self):

        coro = self.sprite.async_move(0.1, 0, speed=1_000_000, fps=1)
        self._run_coroutines(coro)

        self.assert_almost_equal_anchor(self.sprite.anchor, (0.1, 0), places=1)



class TestAsyncMoveToAnimation(AsyncAnimationBase):

    def setUp(self):

        super().setUp()
        self.sprite = base.Sprite(canvas=self.canvas, shape=None, anchor=(80, 60))


    def test_async_move_to_with_speed_moves_anchor(self):

        coro = self.sprite.async_move_to(40, 30, speed=50, fps=10)
        self._run_coroutines(coro)

        self.assert_almost_equal_anchor(self.sprite.anchor, (40, 30), places=1)


    def test_async_move_to_with_speed_calls_canvas_move_and_asyncio_sleep(self):

        coro = self.sprite.async_move_to(40, 30, speed=50, fps=10)
        self._run_coroutines(coro)

        # Given that the move distance is 50 and the speed is 50, animation
        # duration is 1 second. At 10 fps, 10 frames must be generated: each
        # with a call to canvas.move of 1/10th the distance and an await of
        # asyncio.sleep of 1/10th the duration.

        canvas_move_calls = self.canvas.move.call_args_list
        self.assertEqual(len(canvas_move_calls), 10, 'canvas.move call count')
        for call in canvas_move_calls:
            _shape_id, dx, dy = call.args
            self.assertAlmostEqual(dx, -4, places=1)
            self.assertAlmostEqual(dy, -3, places=1)

        asyncio_sleep_call_args = self.asyncio.sleep_call_args
        self.assertEqual(len(asyncio_sleep_call_args), 10, 'asyncio.sleep await count')
        for sleep_duration in asyncio_sleep_call_args:
            self.assertAlmostEqual(sleep_duration, 0.1, places=3)

        # TODO: A more correct test would check that canvas.move calls and
        # asyncio.sleep awaits are called in alternating turns.


    def test_async_move_to_with_speed_and_easing_progresses_non_linearly(self):

        def easing(progress):
            return 0 if progress < 0.5 else 1

        coro = self.sprite.async_move_to(40, 30, speed=50, fps=10, easing=easing)
        self._run_coroutines(coro)

        # canvas.move should have been called 10 times:
        # - First 4 with no movement.
        # - 5th with the whole movement.
        # - Remaining with no movement.

        canvas_move_calls = self.canvas.move.call_args_list
        self.assertEqual(len(canvas_move_calls), 10, 'canvas.move call count')
        for call in canvas_move_calls[:4]:
            _shape_id, dx, dy = call.args
            self.assertAlmostEqual(dx, 0, places=1)
            self.assertAlmostEqual(dy, 0, places=1)

        _shape_id, dx, dy = canvas_move_calls[4].args
        self.assertAlmostEqual(dx, -40, places=1)
        self.assertAlmostEqual(dy, -30, places=1)

        for call in canvas_move_calls[5:]:
            _shape_id, dx, dy = call.args
            self.assertAlmostEqual(dx, 0, places=1)
            self.assertAlmostEqual(dy, 0, places=1)


    def test_async_move_to_with_speed_calls_callback(self):

        data = []
        async def cb(*args):
            data.append(args)

        coro = self.sprite.async_move_to(40, 30, speed=50, fps=10, callback=cb)
        self._run_coroutines(coro)

        # Data should have 10 (progress, (x, y)) tuples:
        self.assertEqual(len(data), 10, 'callback count')
        for i, (progress, (x, y)) in enumerate(data, start=1):
            self.assertAlmostEqual(progress, i/10, places=3)
            self.assertAlmostEqual(x, 80-40*progress, places=1)
            self.assertAlmostEqual(y, 60-30*progress, places=1)


    def test_async_move_to_with_high_speed_and_nearly_zero_frames_works(self):

        coro = self.sprite.async_move_to(80.1, 60, speed=1_000_000, fps=1)
        self._run_coroutines(coro)

        self.assert_almost_equal_anchor(self.sprite.anchor, (80.1, 60), places=1)



class TestAsyncRotateAnimation(AsyncAnimationBase):

    def setUp(self):

        super().setUp()
        self.sprite = base.Sprite(canvas=self.canvas, shape=None)


    def test_async_direct_rotate_with_speed_updates_angle(self):

        coro = self.sprite.async_rotate(30, speed=30, fps=10)
        self._run_coroutines(coro)

        self.assertAlmostEqual(self.sprite.angle, 30, places=1)


    def test_async_rotate_with_speed_calls_asyncio_sleep(self):

        coro = self.sprite.async_rotate(30, speed=30, fps=10)
        self._run_coroutines(coro)

        # Given that the move "distance" is 30 and the speed is 30, animation
        # duration is 1 second. At 10 fps, 10 frames must be generated: each
        # with a an await of asyncio.sleep of 1/10th the duration.

        asyncio_sleep_call_args = self.asyncio.sleep_call_args
        self.assertEqual(len(asyncio_sleep_call_args), 10, 'asyncio.sleep await count')
        for sleep_duration in asyncio_sleep_call_args:
            self.assertAlmostEqual(sleep_duration, 0.1, places=3)


    def test_async_rotate_with_speed_calls_callback(self):

        data = []
        async def cb(*args):
            data.append(args)

        coro = self.sprite.async_rotate(30, speed=30, fps=10, callback=cb)
        self._run_coroutines(coro)

        # Data should have 10 (progress, angle) tuples:
        self.assertEqual(len(data), 10, 'callback count')
        for i, (progress, angle) in enumerate(data, start=1):
            self.assertAlmostEqual(progress, i/10, places=3)
            self.assertAlmostEqual(angle, 30*progress, places=1)


    def test_async_rotate_with_high_speed_and_nearly_zero_frames_works(self):

        coro = self.sprite.async_rotate(0.1, speed=1_000_000, fps=1)
        self._run_coroutines(coro)

        self.assertAlmostEqual(self.sprite.angle, 0.1, places=1)



class TestAsyncRotateToAnimation(AsyncAnimationBase):

    def setUp(self):

        super().setUp()
        self.sprite = base.Sprite(canvas=self.canvas, shape=None, angle=40)


    def test_async_rotate_to_with_speed_updates_angle(self):

        coro = self.sprite.async_rotate_to(30, speed=10, fps=10)
        self._run_coroutines(coro)

        self.assertAlmostEqual(self.sprite.angle, 30, places=1)


    def test_async_rotate_to_with_speed_calls_asyncio_sleep(self):

        coro = self.sprite.async_rotate_to(30, speed=10, fps=10)
        self._run_coroutines(coro)

        # Given that the move "distance" is 10 and the speed is 10, animation
        # duration is 1 second. At 10 fps, 10 frames must be generated: each
        # with a call to asyncio.sleep of 1/10th the duration.

        asyncio_sleep_call_args = self.asyncio.sleep_call_args
        self.assertEqual(len(asyncio_sleep_call_args), 10, 'asyncio.sleep await count')
        for sleep_duration in asyncio_sleep_call_args:
            self.assertAlmostEqual(sleep_duration, 0.1, places=3)


    def test_async_rotate_to_with_speed_calls_callback(self):

        data = []
        async def cb(*args):
            data.append(args)

        coro = self.sprite.async_rotate_to(30, speed=10, fps=10, callback=cb)
        self._run_coroutines(coro)

        # Data should have 10 (progress, angle) tuples:
        self.assertEqual(len(data), 10, 'callback count')
        for i, (progress, angle) in enumerate(data, start=1):
            self.assertAlmostEqual(progress, i/10, places=3)
            self.assertAlmostEqual(angle, 40-10*progress, places=1)


    def test_async_rotate_to_takes_the_shortest_path_350_to_10(self):

        sprite = base.Sprite(canvas=self.canvas, shape=None, angle=350)

        angles = []
        async def cb(_progress, angle):
            angles.append(angle)

        coro = sprite.async_rotate_to(10, speed=1, fps=1, callback=cb)
        self._run_coroutines(coro)

        # Stored angles should grow from 351 to 359, then from 0 to 10
        self.assertEqual(angles, [*range(351, 360), *range(11)])


    def test_async_rotate_to_takes_the_shortest_path_10_to_350(self):

        sprite = base.Sprite(canvas=self.canvas, shape=None, angle=10)

        angles = []
        async def cb(_progress, angle):
            angles.append(angle)

        coro = sprite.async_rotate_to(350, speed=1, fps=1, callback=cb)
        self._run_coroutines(coro)

        # Stored angles should decrease from 9 to 0, then from 359 to 350.
        self.assertEqual(angles, [*range(9, -1, -1), *range(359, 349, -1)])


    def test_async_rotate_to_with_high_speed_and_nearly_zero_frames_works(self):

        coro = self.sprite.async_rotate_to(40.1, speed=1_000_000, fps=1)
        self._run_coroutines(coro)

        self.assertAlmostEqual(self.sprite.angle, 40.1, places=1)



class TestAsyncAnimationConcurrency(AsyncAnimationBase):

    def setUp(self):

        super().setUp()
        self.sprite = base.Sprite(canvas=self.canvas, shape=None)


    def test_concurrent_async_move_works(self):

        coro_h = self.sprite.async_move(40, 0, speed=40, fps=10)
        coro_v = self.sprite.async_move(0, 30, speed=30, fps=10)

        self._run_coroutines(coro_h, coro_v)

        self.assert_almost_equal_anchor(self.sprite.anchor, (40, 30), places=1)


    def test_concurrent_async_rotate_works(self):

        coro_one = self.sprite.async_rotate(20, speed=20, fps=10)
        coro_two = self.sprite.async_rotate(10, speed=10, fps=10)

        self._run_coroutines(coro_one, coro_two)

        self.assertAlmostEqual(self.sprite.angle, 30, places=1)


    def test_concurrent_async_move_and_async_rotate_works(self):

        coros = (
            self.sprite.async_move(40, 0, speed=40, fps=10),
            self.sprite.async_move(0, 30, speed=30, fps=10),
            self.sprite.async_rotate(10, speed=10, fps=10),
            self.sprite.async_rotate(20, speed=20, fps=10),
        )

        self._run_coroutines(*coros)

        self.assert_almost_equal_anchor(self.sprite.anchor, (40, 30), places=1)
        self.assertAlmostEqual(self.sprite.angle, 30, places=1)


    def test_concurrent_async_move_and_async_rotate_to_works(self):

        coros = (
            self.sprite.async_move(40, 0, speed=40, fps=10),
            self.sprite.async_move(0, 30, speed=30, fps=10),
            self.sprite.async_rotate_to(30, speed=30, fps=10),
        )

        self._run_coroutines(*coros)

        self.assert_almost_equal_anchor(self.sprite.anchor, (40, 30), places=1)
        self.assertAlmostEqual(self.sprite.angle, 30, places=1)


    def test_concurrent_async_move_to_and_async_rotate_to_works(self):

        coros = (
            self.sprite.async_move_to(40, 30, speed=50, fps=10),
            self.sprite.async_rotate_to(30, speed=30, fps=10),
        )

        self._run_coroutines(*coros)

        self.assert_almost_equal_anchor(self.sprite.anchor, (40, 30), places=1)
        self.assertAlmostEqual(self.sprite.angle, 30, places=1)


    def test_concurrent_async_move_to_and_async_rotate_works(self):

        coros = (
            self.sprite.async_move_to(40, 30, speed=50, fps=10),
            self.sprite.async_rotate(10, speed=10, fps=10),
            self.sprite.async_rotate(20, speed=20, fps=10),
        )

        self._run_coroutines(*coros)

        self.assert_almost_equal_anchor(self.sprite.anchor, (40, 30), places=1)
        self.assertAlmostEqual(self.sprite.angle, 30, places=1)


    def test_concurrent_async_move_to_fails(self):

        coro_h = self.sprite.async_move_to(40, 0, speed=40, fps=10)
        coro_v = self.sprite.async_move_to(0, 30, speed=30, fps=10)

        with self.assertRaises(base.AnimationError):
            self._run_coroutines(coro_h, coro_v)


    def test_async_move_fails_with_running_async_move_to(self):

        coro_async_move_to = self.sprite.async_move_to(40, 0, speed=40, fps=10)
        coro_async_move = self.sprite.async_move(0, 30, speed=30, fps=10)

        with self.assertRaises(base.AnimationError):
            self._run_coroutines(coro_async_move_to, coro_async_move)


    def test_async_move_to_fails_with_running_async_move(self):

        coro_async_move = self.sprite.async_move(0, 30, speed=30, fps=10)
        coro_async_move_to = self.sprite.async_move_to(40, 0, speed=40, fps=10)

        with self.assertRaises(base.AnimationError):
            self._run_coroutines(coro_async_move, coro_async_move_to)


    def test_concurrent_async_rotate_to_fails(self):

        coro_one = self.sprite.async_rotate_to(10, speed=10, fps=10)
        coro_two = self.sprite.async_rotate_to(20, speed=20, fps=10)

        with self.assertRaises(base.AnimationError):
            self._run_coroutines(coro_one, coro_two)


    def test_async_rotate_fails_with_running_async_rotate_to(self):

        coro_async_rotate_to = self.sprite.async_rotate_to(30, speed=30, fps=10)
        coro_async_rotate = self.sprite.async_rotate(10, speed=10, fps=10)

        with self.assertRaises(base.AnimationError):
            self._run_coroutines(coro_async_rotate_to, coro_async_rotate)


    def test_async_rotate_to_fails_with_running_async_rotate(self):

        coro_async_rotate = self.sprite.async_rotate(10, speed=10, fps=10)
        coro_async_rotate_to = self.sprite.async_rotate_to(30, speed=30, fps=10)

        with self.assertRaises(base.AnimationError):
            self._run_coroutines(coro_async_rotate, coro_async_rotate_to)



class SyncAnimationBase(test_base.TestCase):

    def setUp(self):

        self.canvas = fake_tkinter.FakeCanvas()

        self.time = mock.Mock()
        self._exit_stack = contextlib.ExitStack()
        self._exit_stack.enter_context(
            mock.patch('aturtle.sprites.base.time', self.time)
        )


    def tearDown(self):

        self._exit_stack.close()



class TestSyncMoveAnimation(SyncAnimationBase):

    def setUp(self):

        super().setUp()
        self.sprite = base.Sprite(canvas=self.canvas, shape=None, anchor=(0, 0))


    def test_sync_move_with_speed_moves_anchor(self):

        self.sprite.sync_move(40, 30, speed=50, fps=10)
        self.assert_almost_equal_anchor(self.sprite.anchor, (40, 30), places=1)


    def test_sync_move_with_speed_calls_canvas_move_and_time_sleep(self):

        self.sprite.sync_move(40, 30, speed=50, fps=10)

        # Given that the move distance is 50 and the speed is 50, animation
        # duration is 1 second. At 10 fps, 10 frames must be generated: each
        # with a call to canvas.move of 1/10th the distance and an await of
        # asyncio.sleep of 1/10th the duration.

        canvas_move_calls = self.canvas.move.call_args_list
        self.assertEqual(len(canvas_move_calls), 10, 'canvas.move call count')
        for call in canvas_move_calls:
            _shape_id, dx, dy = call.args
            self.assertAlmostEqual(dx, 4, places=1)
            self.assertAlmostEqual(dy, 3, places=1)

        time_sleep_call_args = self.time.sleep.call_args_list
        self.assertEqual(len(time_sleep_call_args), 10, 'time.sleep await count')
        for call_args in time_sleep_call_args:
            self.assertAlmostEqual(call_args.args[0], 0.1, places=3)

        # TODO: A more correct test would check that canvas.move calls and
        # asyncio.sleep awaits are called in alternating turns.


    def test_sync_move_with_speed_and_easing_progresses_non_linearly(self):

        def easing(progress):
            return 0 if progress < 0.5 else 1

        self.sprite.sync_move(40, 30, speed=50, fps=10, easing=easing)

        # canvas.move should have been called 10 times:
        # - First 4 with no movement.
        # - 5th with the whole movement.
        # - Remaining with no movement.

        canvas_move_calls = self.canvas.move.call_args_list
        self.assertEqual(len(canvas_move_calls), 10, 'canvas.move call count')
        for call in canvas_move_calls[:4]:
            _shape_id, dx, dy = call.args
            self.assertAlmostEqual(dx, 0, places=1)
            self.assertAlmostEqual(dy, 0, places=1)

        _shape_id, dx, dy = canvas_move_calls[4].args
        self.assertAlmostEqual(dx, 40, places=1)
        self.assertAlmostEqual(dy, 30, places=1)

        for call in canvas_move_calls[5:]:
            _shape_id, dx, dy = call.args
            self.assertAlmostEqual(dx, 0, places=1)
            self.assertAlmostEqual(dy, 0, places=1)


    def test_sync_move_with_speed_calls_callback(self):

        data = []
        def cb(*args):
            data.append(args)

        self.sprite.sync_move(40, 30, speed=50, fps=10, callback=cb)

        # Data should have 10 (progress, (x, y)) tuples:
        self.assertEqual(len(data), 10, 'callback count')
        for i, (progress, (x, y)) in enumerate(data, start=1):
            self.assertAlmostEqual(progress, i/10, places=3)
            self.assertAlmostEqual(x, 40*progress, places=1)
            self.assertAlmostEqual(y, 30*progress, places=1)


    def test_sync_move_with_high_speed_and_nearly_zero_frames_works(self):

        self.sprite.sync_move(0.1, 0, speed=1_000_000, fps=1)
        self.assert_almost_equal_anchor(self.sprite.anchor, (0.1, 0), places=1)


class TestSyncMoveToAnimation(SyncAnimationBase):

    def setUp(self):

        super().setUp()
        self.sprite = base.Sprite(canvas=self.canvas, shape=None, anchor=(80, 60))


    def test_sync_move_to_with_speed_moves_anchor(self):

        self.sprite.sync_move_to(40, 30, speed=50, fps=10)

        self.assert_almost_equal_anchor(self.sprite.anchor, (40, 30), places=1)


    def test_sync_move_to_with_speed_calls_canvas_move_and_time_sleep(self):

        self.sprite.sync_move_to(40, 30, speed=50, fps=10)

        # Given that the move distance is 50 and the speed is 50, animation
        # duration is 1 second. At 10 fps, 10 frames must be generated: each
        # with a call to canvas.move of 1/10th the distance and an await of
        # asyncio.sleep of 1/10th the duration.

        canvas_move_calls = self.canvas.move.call_args_list
        self.assertEqual(len(canvas_move_calls), 10, 'canvas.move call count')
        for call in canvas_move_calls:
            _shape_id, dx, dy = call.args
            self.assertAlmostEqual(dx, -4, places=1)
            self.assertAlmostEqual(dy, -3, places=1)

        time_sleep_call_args = self.time.sleep.call_args_list
        self.assertEqual(len(time_sleep_call_args), 10, 'time.sleep await count')
        for call_args in time_sleep_call_args:
            self.assertAlmostEqual(call_args.args[0], 0.1, places=3)

        # TODO: A more correct test would check that canvas.move calls and
        # asyncio.sleep awaits are called in alternating turns.


    def test_sync_move_to_with_speed_and_easing_progresses_non_linearly(self):

        def easing(progress):
            return 0 if progress < 0.5 else 1

        self.sprite.sync_move_to(40, 30, speed=50, fps=10, easing=easing)

        # canvas.move should have been called 10 times:
        # - First 4 with no movement.
        # - 5th with the whole movement.
        # - Remaining with no movement.

        canvas_move_calls = self.canvas.move.call_args_list
        self.assertEqual(len(canvas_move_calls), 10, 'canvas.move call count')
        for call in canvas_move_calls[:4]:
            _shape_id, dx, dy = call.args
            self.assertAlmostEqual(dx, 0, places=1)
            self.assertAlmostEqual(dy, 0, places=1)

        _shape_id, dx, dy = canvas_move_calls[4].args
        self.assertAlmostEqual(dx, -40, places=1)
        self.assertAlmostEqual(dy, -30, places=1)

        for call in canvas_move_calls[5:]:
            _shape_id, dx, dy = call.args
            self.assertAlmostEqual(dx, 0, places=1)
            self.assertAlmostEqual(dy, 0, places=1)


    def test_sync_move_to_with_speed_calls_callback(self):

        data = []
        def cb(*args):
            data.append(args)

        self.sprite.sync_move_to(40, 30, speed=50, fps=10, callback=cb)

        # Data should have 10 (progress, (x, y)) tuples:
        self.assertEqual(len(data), 10, 'callback count')
        for i, (progress, (x, y)) in enumerate(data, start=1):
            self.assertAlmostEqual(progress, i/10, places=3)
            self.assertAlmostEqual(x, 80-40*progress, places=1)
            self.assertAlmostEqual(y, 60-30*progress, places=1)


    def test_sync_move_to_with_high_speed_and_nearly_zero_frames_works(self):

        self.sprite.sync_move_to(80.1, 60, speed=1_000_000, fps=1)
        self.assert_almost_equal_anchor(self.sprite.anchor, (80.1, 60), places=1)



class TestSyncRotateAnimation(SyncAnimationBase):

    def setUp(self):

        super().setUp()
        self.sprite = base.Sprite(canvas=self.canvas, shape=None)


    def test_sync_rotate_with_speed_updates_angle(self):

        self.sprite.sync_rotate(30, speed=30, fps=10)

        self.assertAlmostEqual(self.sprite.angle, 30, places=1)


    def test_sync_rotate_with_speed_calls_time_sleep(self):

        self.sprite.sync_rotate(30, speed=30, fps=10)

        # Given that the move "distance" is 30 and the speed is 30, animation
        # duration is 1 second. At 10 fps, 10 frames must be generated: each
        # with a an await of asyncio.sleep of 1/10th the duration.

        time_sleep_call_args = self.time.sleep.call_args_list
        self.assertEqual(len(time_sleep_call_args), 10, 'asyncio.sleep await count')
        for call_args in time_sleep_call_args:
            self.assertAlmostEqual(call_args.args[0], 0.1, places=3)


    def test_sync_rotate_with_speed_calls_callback(self):

        data = []
        def cb(*args):
            data.append(args)

        self.sprite.sync_rotate(30, speed=30, fps=10, callback=cb)

        # Data should have 10 (progress, angle) tuples:
        self.assertEqual(len(data), 10, 'callback count')
        for i, (progress, angle) in enumerate(data, start=1):
            self.assertAlmostEqual(progress, i/10, places=3)
            self.assertAlmostEqual(angle, 30*progress, places=1)


    def test_sync_rotate_with_high_speed_and_nearly_zero_frames_works(self):

        self.sprite.sync_rotate(0.1, speed=1_000_000, fps=1)
        self.assertAlmostEqual(self.sprite.angle, 0.1, places=1)



class TestSyncRotateToAnimation(SyncAnimationBase):

    def setUp(self):

        super().setUp()
        self.sprite = base.Sprite(canvas=self.canvas, shape=None, angle=40)


    def test_sync_rotate_to_with_speed_updates_angle(self):

        self.sprite.sync_rotate_to(30, speed=10, fps=10)

        self.assertAlmostEqual(self.sprite.angle, 30, places=1)


    def test_sync_rotate_to_with_speed_calls_time_sleep(self):

        self.sprite.sync_rotate_to(30, speed=10, fps=10)

        # Given that the move "distance" is 10 and the speed is 10, animation
        # duration is 1 second. At 10 fps, 10 frames must be generated: each
        # with a call to asyncio.sleep of 1/10th the duration.

        time_sleep_call_args = self.time.sleep.call_args_list
        self.assertEqual(len(time_sleep_call_args), 10, 'asyncio.sleep await count')
        for call_args in time_sleep_call_args:
            self.assertAlmostEqual(call_args.args[0], 0.1, places=3)


    def test_sync_rotate_to_with_speed_calls_callback(self):

        data = []
        def cb(*args):
            data.append(args)

        self.sprite.sync_rotate_to(30, speed=10, fps=10, callback=cb)

        # Data should have 10 (progress, angle) tuples:
        self.assertEqual(len(data), 10, 'callback count')
        for i, (progress, angle) in enumerate(data, start=1):
            self.assertAlmostEqual(progress, i/10, places=3)
            self.assertAlmostEqual(angle, 40-10*progress, places=1)


    def test_sync_rotate_to_takes_the_shortest_path_350_to_10(self):

        sprite = base.Sprite(canvas=self.canvas, shape=None, angle=350)

        angles = []
        def cb(_progress, angle):
            angles.append(angle)

        sprite.sync_rotate_to(10, speed=1, fps=1, callback=cb)

        # Stored angles should grow from 351 to 359, then from 0 to 10
        self.assertEqual(angles, [*range(351, 360), *range(11)])


    def test_sync_rotate_to_takes_the_shortest_path_10_to_350(self):

        sprite = base.Sprite(canvas=self.canvas, shape=None, angle=10)

        angles = []
        def cb(_progress, angle):
            angles.append(angle)

        sprite.sync_rotate_to(350, speed=1, fps=1, callback=cb)

        # Stored angles should decrease from 9 to 0, then from 359 to 350.
        self.assertEqual(angles, [*range(9, -1, -1), *range(359, 349, -1)])

    def test_sync_rotate_to_with_high_speed_and_nearly_zero_frames_works(self):

        self.sprite.sync_rotate_to(40.1, speed=1_000_000, fps=1)
        self.assertAlmostEqual(self.sprite.angle, 40.1, places=1)




class TestRegressionSpriteInitializedWithUpdateTrue(test_base.TestCase):

    def setUp(self):

        self.canvas = fake_tkinter.FakeCanvas()
        self.sprite = base.Sprite(self.canvas, shape=None, update=True)


    def test_direct_move_with_update_False_doesnt_call_canvas_update(self):

        self.sprite.direct_move(30, 40, update=False)
        self.canvas.update.assert_not_called()


    def test_direct_rotate_around_with_update_False_doesnt_call_canvas_update(self):

        self.sprite.direct_rotate(30, around=(10, 10), update=False)
        self.canvas.update.assert_not_called()
