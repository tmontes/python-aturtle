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


    def test_move_moves_anchor(self):

        sprite = base.Sprite(canvas=self.canvas, shape=None)
        sprite.move(42, 24)
        self.assert_almost_equal_anchor(sprite.anchor, (42, 24), places=1)


    def test_move_moves_anchor_relative(self):

        sprite = base.Sprite(canvas=self.canvas, shape=None)
        sprite.move(42, 0)
        sprite.move(0, 24)
        self.assert_almost_equal_anchor(sprite.anchor, (42, 24), places=1)


    def test_move_does_not_change_angle(self):

        sprite = base.Sprite(canvas=self.canvas, shape=None)
        sprite.move(42, 24)
        self.assertAlmostEqual(sprite.angle, 0, places=1)


    def test_move_to_moves_anchor(self):

        sprite = base.Sprite(canvas=self.canvas, shape=None)
        sprite.move_to(42, 24)
        self.assert_almost_equal_anchor(sprite.anchor, (42, 24), places=1)


    def test_move_to_moves_anchor_absolute(self):

        sprite = base.Sprite(canvas=self.canvas, shape=None)
        sprite.move_to(42, 0)
        sprite.move_to(0, 24)
        self.assert_almost_equal_anchor(sprite.anchor, (0, 24), places=1)


    def test_move_to_does_not_change_angle(self):

        sprite = base.Sprite(canvas=self.canvas, shape=None)
        sprite.move_to(42, 24)
        self.assertAlmostEqual(sprite.angle, 0, places=1)


    def test_rotate_does_not_move_anchor(self):

        sprite = base.Sprite(canvas=self.canvas, shape=None)
        sprite.rotate(90)
        self.assert_almost_equal_anchor(sprite.anchor, (0, 0), places=1)


    def test_rotate_around_moves_anchor(self):

        sprite = base.Sprite(canvas=self.canvas, shape=None)
        sprite.rotate(180, around=(1, 1))
        self.assert_almost_equal_anchor(sprite.anchor, (2, 2), places=1)


    def test_rotate_around_moves_anchor_relative(self):

        sprite = base.Sprite(canvas=self.canvas, shape=None)
        sprite.rotate(90, around=(1, 1))
        sprite.rotate(90, around=(1, 1))
        self.assert_almost_equal_anchor(sprite.anchor, (2, 2), places=1)


    def test_rotate_changes_angle(self):

        sprite = base.Sprite(canvas=self.canvas, shape=None)
        sprite.rotate(90)
        self.assertAlmostEqual(sprite.angle, 90, places=1)


    def test_rotate_changes_angle_relative(self):

        sprite = base.Sprite(canvas=self.canvas, shape=None)
        sprite.rotate(45)
        sprite.rotate(45)
        self.assertAlmostEqual(sprite.angle, 90, places=1)


    def test_rotate_around_changes_angle(self):

        sprite = base.Sprite(canvas=self.canvas, shape=None)
        sprite.rotate(90, around=(1, 1))
        self.assertAlmostEqual(sprite.angle, 90, places=1)


    def test_rotate_to_does_not_move_anchor(self):

        sprite = base.Sprite(canvas=self.canvas, shape=None)
        sprite.rotate_to(90)
        self.assert_almost_equal_anchor(sprite.anchor, (0, 0), places=1)


    def test_rotate_to_around_moves_anchor(self):

        sprite = base.Sprite(canvas=self.canvas, shape=None)
        sprite.rotate_to(180, around=(1, 1))
        self.assert_almost_equal_anchor(sprite.anchor, (2, 2), places=1)


    def test_rotate_to_around_moves_anchor_absolute(self):

        sprite = base.Sprite(canvas=self.canvas, shape=None)
        sprite.rotate_to(90, around=(1, 1))
        sprite.rotate_to(180, around=(1, 1))
        self.assert_almost_equal_anchor(sprite.anchor, (2, 2), places=1)


    def test_rotate_to_changes_angle(self):

        sprite = base.Sprite(canvas=self.canvas, shape=None)
        sprite.rotate_to(90)
        self.assertAlmostEqual(sprite.angle, 90, places=1)


    def test_rotate_to_changes_angle_absolute(self):

        sprite = base.Sprite(canvas=self.canvas, shape=None)
        sprite.rotate_to(20)
        sprite.rotate_to(90)
        self.assertAlmostEqual(sprite.angle, 90, places=1)


    def test_rotate_to_around_changes_angle(self):

        sprite = base.Sprite(canvas=self.canvas, shape=None)
        sprite.rotate_to(90, around=(1, 1))
        self.assertAlmostEqual(sprite.angle, 90, places=1)


    def test_update_calls_canvas_update(self):

        sprite = base.Sprite(canvas=self.canvas, shape=None)
        sprite.update()
        self.canvas.update.assert_called_once_with()


    def test_move_with_no_update_calls_canvas_update(self):

        sprite = base.Sprite(canvas=self.canvas, shape=None)
        sprite.move(42, 24)
        self.canvas.update.assert_not_called()


    def test_move_with_update_calls_canvas_update(self):

        sprite = base.Sprite(canvas=self.canvas, shape=None)
        sprite.move(42, 24, update=True)
        self.canvas.update.assert_called_once_with()


    def test_move_to_with_no_update_calls_canvas_update(self):

        sprite = base.Sprite(canvas=self.canvas, shape=None)
        sprite.move_to(42, 24)
        self.canvas.update.assert_not_called()


    def test_move_to_with_update_calls_canvas_update(self):

        sprite = base.Sprite(canvas=self.canvas, shape=None)
        sprite.move_to(42, 24, update=True)
        self.canvas.update.assert_called_once_with()


    def test_rotate_with_no_update_calls_canvas_update(self):

        sprite = base.Sprite(canvas=self.canvas, shape=None)
        sprite.rotate(42)
        self.canvas.update.assert_not_called()


    def test_rotate_with_update_calls_canvas_update(self):

        sprite = base.Sprite(canvas=self.canvas, shape=None)
        sprite.rotate(42, update=True)
        self.canvas.update.assert_called_once_with()


    def test_rotate_to_with_no_update_calls_canvas_update(self):

        sprite = base.Sprite(canvas=self.canvas, shape=None)
        sprite.rotate_to(42)
        self.canvas.update.assert_not_called()


    def test_rotate_to_with_update_calls_canvas_update(self):

        sprite = base.Sprite(canvas=self.canvas, shape=None)
        sprite.rotate_to(42, update=True)
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


    def test_move_with_no_args_does_not_move_anchor(self):

        self.sprite.move()
        self.assert_almost_equal_anchor(self.sprite.anchor, (42, 24), places=1)


    def test_move_moves_anchor(self):

        self.sprite.move(-42, -24)
        self.assert_almost_equal_anchor(self.sprite.anchor, (0, 0), places=1)


    def test_move_moves_anchor_relative(self):

        self.sprite.move(-42, 0)
        self.sprite.move(0, -24)
        self.assert_almost_equal_anchor(self.sprite.anchor, (0, 0), places=1)


    def test_move_does_not_change_angle(self):

        self.sprite.move(42, 24)
        self.assertAlmostEqual(self.sprite.angle, 42, places=1)


    def test_move_to_moves_anchor(self):

        self.sprite.move_to(20, 10)
        self.assert_almost_equal_anchor(self.sprite.anchor, (20, 10), places=1)


    def test_move_to_moves_anchor_absolute(self):

        self.sprite.move_to(42, 0)
        self.sprite.move_to(0, 24)
        self.assert_almost_equal_anchor(self.sprite.anchor, (0, 24), places=1)


    def test_move_to_does_not_change_angle(self):

        self.sprite.move_to(42, 24)
        self.assertAlmostEqual(self.sprite.angle, 42, places=1)


    def test_rotate_does_not_move_anchor(self):

        self.sprite.rotate(90)
        self.assert_almost_equal_anchor(self.sprite.anchor, (42, 24), places=1)


    def test_rotate_around_moves_anchor(self):

        self.sprite.rotate(180, around=(0, 0))
        self.assert_almost_equal_anchor(self.sprite.anchor, (-42, -24), places=1)


    def test_rotate_around_moves_anchor_relative(self):

        self.sprite.rotate(90, around=(0, 0))
        self.sprite.rotate(90, around=(0, 0))
        self.assert_almost_equal_anchor(self.sprite.anchor, (-42, -24), places=1)


    def test_rotate_changes_angle(self):

        self.sprite.rotate(-42)
        self.assertAlmostEqual(self.sprite.angle, 0, places=1)


    def test_rotate_changes_angle_relative(self):

        self.sprite.rotate(-40)
        self.sprite.rotate(-2)
        self.assertAlmostEqual(self.sprite.angle, 0, places=1)


    def test_rotate_around_changes_angle(self):

        self.sprite.rotate(-42, around=(1, 1))
        self.assertAlmostEqual(self.sprite.angle, 0, places=1)


    def test_rotate_to_does_not_move_anchor(self):

        self.sprite.rotate_to(90)
        self.assert_almost_equal_anchor(self.sprite.anchor, (42, 24), places=1)


    def test_rotate_to_around_moves_anchor(self):

        self.sprite.rotate_to(42+180, around=(0, 0))
        self.assert_almost_equal_anchor(self.sprite.anchor, (-42, -24), places=1)


    def test_rotate_to_around_moves_anchor_absolute(self):

        self.sprite.rotate_to(90, around=(0, 0))
        self.sprite.rotate_to(42+180, around=(0, 0))
        self.assert_almost_equal_anchor(self.sprite.anchor, (-42, -24), places=1)


    def test_rotate_to_changes_angle(self):

        self.sprite.rotate_to(90)
        self.assertAlmostEqual(self.sprite.angle, 90, places=1)


    def test_rotate_to_changes_angle_absolute(self):

        self.sprite.rotate_to(20)
        self.sprite.rotate_to(90)
        self.assertAlmostEqual(self.sprite.angle, 90, places=1)


    def test_rotate_to_around_changes_angle(self):

        self.sprite.rotate_to(90, around=(1, 1))
        self.assertAlmostEqual(self.sprite.angle, 90, places=1)


    def test_update_calls_canvas_update(self):

        self.sprite.update()
        self.canvas.update.assert_called_once_with()


    def test_move_with_no_update_calls_canvas_update(self):

        self.sprite.move(42, 24)
        self.canvas.update.assert_not_called()


    def test_move_with_update_calls_canvas_update(self):

        self.sprite.move(42, 24, update=True)
        self.canvas.update.assert_called_once_with()


    def test_move_to_with_no_update_calls_canvas_update(self):

        self.sprite.move_to(42, 24)
        self.canvas.update.assert_not_called()


    def test_move_to_with_update_calls_canvas_update(self):

        self.sprite.move_to(42, 24, update=True)
        self.canvas.update.assert_called_once_with()


    def test_rotate_with_no_update_calls_canvas_update(self):

        self.sprite.rotate(42)
        self.canvas.update.assert_not_called()


    def test_rotate_with_update_calls_canvas_update(self):

        self.sprite.rotate(42, update=True)
        self.canvas.update.assert_called_once_with()


    def test_rotate_to_with_no_update_calls_canvas_update(self):

        self.sprite.rotate_to(42)
        self.canvas.update.assert_not_called()


    def test_rotate_to_with_update_calls_canvas_update(self):

        self.sprite.rotate_to(42, update=True)
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


    def test_a_move_with_speed_None_moves_anchor(self):

        coro = self.sprite.a_move(40, 30, speed=None, fps=10)
        self._run_coroutines(coro)

        self.assert_almost_equal_anchor(self.sprite.anchor, (40, 30), places=1)


    def test_a_move_with_speed_None_is_single_step_and_synchronous(self):

        coro = self.sprite.a_move(40, 30, speed=None, fps=10)
        self._run_coroutines(coro)

        self.canvas.move.assert_called_once_with(None, 40, 30)
        self.assertFalse(self.asyncio.sleep_call_args, 'asyncio sleep call args')


    def test_a_move_with_speed_moves_anchor(self):

        coro = self.sprite.a_move(40, 30, speed=50, fps=10)
        self._run_coroutines(coro)

        self.assert_almost_equal_anchor(self.sprite.anchor, (40, 30), places=1)


    def test_a_move_with_speed_calls_canvas_move_and_asyncio_sleep(self):

        coro = self.sprite.a_move(40, 30, speed=50, fps=10)
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


    def test_a_move_with_speed_and_easing_progresses_non_linearly(self):

        def easing(progress):
            return 0 if progress < 0.5 else 1

        coro = self.sprite.a_move(40, 30, speed=50, fps=10, easing=easing)
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


    def test_a_move_with_speed_calls_callback(self):

        data = []

        coro = self.sprite.a_move(40, 30, speed=50, fps=10,
                                  callback=lambda *args: data.append(args))
        self._run_coroutines(coro)

        # Data should have 10 (progress, (x, y)) tuples:
        self.assertEqual(len(data), 10, 'callback count')
        for i, (progress, (x, y)) in enumerate(data, start=1):
            self.assertAlmostEqual(progress, i/10, places=3)
            self.assertAlmostEqual(x, 40*progress, places=1)
            self.assertAlmostEqual(y, 30*progress, places=1)


    def test_a_move_with_speed_None_does_not_call_callback(self):

        data = []

        coro = self.sprite.a_move(40, 30, speed=None, fps=10,
                                  callback=lambda *args: data.append(args))
        self._run_coroutines(coro)

        self.assertFalse(data, 'no callbacks expected')


    def test_concurrent_a_move_works(self):


        coro_h = self.sprite.a_move(40, 0, speed=40, fps=10)
        coro_v = self.sprite.a_move(0, 30, speed=30, fps=10)

        self._run_coroutines(coro_h, coro_v)

        self.assert_almost_equal_anchor(self.sprite.anchor, (40, 30), places=1)



class TestAsyncMoveToAnimation(AsyncAnimationBase):

    def setUp(self):

        super().setUp()
        self.sprite = base.Sprite(canvas=self.canvas, shape=None, anchor=(80, 60))


    def test_a_move_to_with_speed_None_moves_anchor(self):

        coro = self.sprite.a_move_to(40, 30, speed=None, fps=10)
        self._run_coroutines(coro)

        self.assert_almost_equal_anchor(self.sprite.anchor, (40, 30), places=1)


    def test_a_move_to_with_speed_None_is_single_step_and_synchronous(self):

        coro = self.sprite.a_move_to(40, 30, speed=None, fps=10)
        self._run_coroutines(coro)

        self.canvas.move.assert_called_once_with(None, -40, -30)
        self.assertFalse(self.asyncio.sleep_call_args, 'asyncio sleep call args')


    def test_a_move_to_with_speed_moves_anchor(self):

        coro = self.sprite.a_move_to(40, 30, speed=50, fps=10)
        self._run_coroutines(coro)

        self.assert_almost_equal_anchor(self.sprite.anchor, (40, 30), places=1)


    def test_a_move_to_with_speed_calls_canvas_move_and_asyncio_sleep(self):

        coro = self.sprite.a_move_to(40, 30, speed=50, fps=10)
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


    def test_a_move_to_with_speed_and_easing_progresses_non_linearly(self):

        def easing(progress):
            return 0 if progress < 0.5 else 1

        coro = self.sprite.a_move_to(40, 30, speed=50, fps=10, easing=easing)
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


    def test_a_move_to_with_speed_calls_callback(self):

        data = []

        coro = self.sprite.a_move_to(40, 30, speed=50, fps=10,
                                     callback=lambda *args: data.append(args))
        self._run_coroutines(coro)

        # Data should have 10 (progress, (x, y)) tuples:
        self.assertEqual(len(data), 10, 'callback count')
        for i, (progress, (x, y)) in enumerate(data, start=1):
            self.assertAlmostEqual(progress, i/10, places=3)
            self.assertAlmostEqual(x, 80-40*progress, places=1)
            self.assertAlmostEqual(y, 60-30*progress, places=1)


    def test_a_move_to_with_speed_None_does_not_call_callback(self):

        data = []

        coro = self.sprite.a_move_to(40, 30, speed=None, fps=10,
                                     callback=lambda *args: data.append(args))
        self._run_coroutines(coro)

        self.assertFalse(data, 'no callbacks expected')


    def test_concurrent_a_move_to_fails(self):


        coro_h = self.sprite.a_move_to(40, 0, speed=40, fps=10)
        coro_v = self.sprite.a_move_to(0, 30, speed=30, fps=10)

        with self.assertRaises(base.AnimationError):
            self._run_coroutines(coro_h, coro_v)


    def test_concurrent_a_move_to_with_a_move_fails(self):

        coro_absolute = self.sprite.a_move_to(40, 0, speed=40, fps=10)
        coro_relative = self.sprite.a_move(0, 30, speed=30, fps=10)

        with self.assertRaises(base.AnimationError):
            self._run_coroutines(coro_absolute, coro_relative)
