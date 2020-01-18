# ----------------------------------------------------------------------------
# Python A-Turtle
# ----------------------------------------------------------------------------
# Copyright (c) Tiago Montes.
# See LICENSE for details.
# ----------------------------------------------------------------------------

import collections
import contextlib
import itertools as it
from unittest import mock

from aturtle import turtle
from aturtle.sprites import base as sprite_base

from . import base
from . import fake_tkinter
from . import fake_sprite
from . import fake_asyncio



class TestTurtle(base.TestCase):

    def setUp(self):

        self.canvas = fake_tkinter.FakeCanvas()
        self.sprite = fake_sprite.FakeSprite(
            canvas=self.canvas,
            anchor=(0, 0),
            angle=0,
        )


    def test_create_turtle_default_down(self):

        t = turtle.Turtle(self.sprite)
        self.assertIs(t.down, True)


    def test_create_turtle_default_line_color(self):

        t = turtle.Turtle(self.sprite)
        self.assertEqual(t.line_color, '#cccccc')


    def test_create_turtle_default_line_width(self):

        t = turtle.Turtle(self.sprite)
        self.assertEqual(t.line_width, 3)


    def test_create_turtle_anchor_from_sprite(self):

        t = turtle.Turtle(self.sprite)
        self.assertEqual(t.anchor, (0, 0))


    def test_create_turtle_angle_from_sprite(self):

        t = turtle.Turtle(self.sprite)
        self.assertEqual(t.angle, 0)


    def test_create_turtle_explicit_down_True(self):

        t = turtle.Turtle(self.sprite, down=True)
        self.assertIs(t.down, True)


    def test_create_turtle_explicit_down_False(self):

        t = turtle.Turtle(self.sprite, down=False)
        self.assertIs(t.down, False)


    def test_create_turtle_explicit_line_color(self):

        t = turtle.Turtle(self.sprite, line_color='orange')
        self.assertEqual(t.line_color, 'orange')


    def test_create_turtle_explicit_line_width(self):

        t = turtle.Turtle(self.sprite, line_width=42)
        self.assertEqual(t.line_width, 42)



class AsyncAnimationBase(base.TestCase):

    def setUp(self):

        self.asyncio = fake_asyncio.FakeAsyncio()
        self._exit_stack = contextlib.ExitStack()
        self._exit_stack.enter_context(
            mock.patch('aturtle.sprites.base.asyncio', self.asyncio)
        )

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



class TestTurtleAsyncRotation(AsyncAnimationBase):

    def setUp(self):

        super().setUp()

        self.canvas = fake_tkinter.FakeCanvas()
        self.sprite = fake_sprite.FakeSprite(
            canvas=self.canvas,
            anchor=(0, 0),
            angle=0,
        )
        self.t = turtle.Turtle(self.sprite)


    def test_async_left_awaits_sprite_async_rotate(self):

        coro = self.t.async_left(90)
        self._run_coroutines(coro)

        self.sprite.async_rotate.assert_awaited_with(
            -90,
            speed=None,
            easing=None,
            fps=None,
            update=None,
        )


    def test_async_left_with_args_awaits_sprite_async_rotate_with_args(self):

        coro = self.t.async_left(
            90,
            speed='speed',
            easing='easing',
            fps='fps',
            update='update',
        )
        self._run_coroutines(coro)

        self.sprite.async_rotate.assert_awaited_with(
            -90,
            speed='speed',
            easing='easing',
            fps='fps',
            update='update',
        )


    def test_async_right_awaits_sprite_async_rotate(self):

        coro = self.t.async_right(90)
        self._run_coroutines(coro)

        self.sprite.async_rotate.assert_awaited_with(
            90,
            speed=None,
            easing=None,
            fps=None,
            update=None,
        )


    def test_async_right_with_args_awaits_sprite_async_rotate_with_args(self):

        coro = self.t.async_right(
            90,
            speed='speed',
            easing='easing',
            fps='fps',
            update='update',
        )
        self._run_coroutines(coro)

        self.sprite.async_rotate.assert_awaited_with(
            90,
            speed='speed',
            easing='easing',
            fps='fps',
            update='update',
        )



class TestTurtleAsyncMovement(AsyncAnimationBase):

    def setUp(self):

        super().setUp()

        self.canvas = fake_tkinter.FakeCanvas()
        self.sprite = fake_sprite.FakeSprite(
            canvas=self.canvas,
            anchor=(0, 0),
            angle=0,
        )


    def test_async_forward_awaits_sprite_async_forward(self):

        t = turtle.Turtle(self.sprite)

        coro = t.async_forward(42)
        self._run_coroutines(coro)

        self.sprite.async_forward.assert_awaited_with(
            42,
            callback=t._async_draw_line,
            speed=None,
            easing=None,
            fps=None,
            update=None,
        )


    def test_async_forward_with_args_awaits_sprite_async_forward_with_args(self):

        t = turtle.Turtle(self.sprite)

        coro = t.async_forward(
            42,
            speed='speed',
            easing='easing',
            fps='fps',
            update='update',
        )
        self._run_coroutines(coro)

        self.sprite.async_forward.assert_awaited_with(
            42,
            callback=t._async_draw_line,
            speed='speed',
            easing='easing',
            fps='fps',
            update='update',
        )


    def test_async_forward_down_draw_line_vs_init_down(self):

        init_downs = (False, True)
        downs = (None, False, True)

        for init_down, down in it.product(init_downs, downs):
            with self.subTest(init_down=init_down, down=down):

                t = turtle.Turtle(self.sprite, down=init_down)

                self.assertIs(t.down, init_down)

                coro = t.async_forward(42, down=down)
                self._run_coroutines(coro)

                self.assertIs(t.down, init_down)

                effective_down = down if down is not None else init_down
                expected_cb = t._async_draw_line if effective_down else None

                self.sprite.async_forward.assert_awaited_with(
                    42,
                    callback=expected_cb,
                    speed=None,
                    easing=None,
                    fps=None,
                    update=None,
                )


    def test_async_backward_awaits_sprite_async_forward(self):

        t = turtle.Turtle(self.sprite)

        coro = t.async_backward(42)
        self._run_coroutines(coro)

        self.sprite.async_forward.assert_awaited_with(
            -42,
            callback=t._async_draw_line,
            speed=None,
            easing=None,
            fps=None,
            update=None,
        )


    def test_async_backward_with_args_awaits_sprite_async_forward_with_args(self):

        t = turtle.Turtle(self.sprite)

        coro = t.async_backward(
            -42,
            speed='speed',
            easing='easing',
            fps='fps',
            update='update',
        )
        self._run_coroutines(coro)

        self.sprite.async_forward.assert_awaited_with(
            42,
            callback=t._async_draw_line,
            speed='speed',
            easing='easing',
            fps='fps',
            update='update',
        )


    def test_async_backward_down_draw_line_vs_init_down(self):

        init_downs = (False, True)
        downs = (None, False, True)

        for init_down, down in it.product(init_downs, downs):
            with self.subTest(init_down=init_down, down=down):

                t = turtle.Turtle(self.sprite, down=init_down)

                self.assertIs(t.down, init_down)

                coro = t.async_backward(42, down=down)
                self._run_coroutines(coro)

                self.assertIs(t.down, init_down)

                effective_down = down if down is not None else init_down
                expected_cb = t._async_draw_line if effective_down else None

                self.sprite.async_forward.assert_awaited_with(
                    -42,
                    callback=expected_cb,
                    speed=None,
                    easing=None,
                    fps=None,
                    update=None,
                )


    def test_async_move_awaits_sprite_async_move(self):

        t = turtle.Turtle(self.sprite)

        coro = t.async_move(42, 24)
        self._run_coroutines(coro)

        self.sprite.async_move.assert_awaited_with(
            42, 24,
            callback=t._async_draw_line,
            speed=None,
            easing=None,
            fps=None,
            update=None,
        )


    def test_async_move_with_args_awaits_sprite_async_move_with_args(self):

        t = turtle.Turtle(self.sprite)

        coro = t.async_move(
            42, 24,
            speed='speed',
            easing='easing',
            fps='fps',
            update='update',
        )
        self._run_coroutines(coro)

        self.sprite.async_move.assert_awaited_with(
            42, 24,
            callback=t._async_draw_line,
            speed='speed',
            easing='easing',
            fps='fps',
            update='update',
        )


    def test_async_move_down_draw_line_vs_init_down(self):

        init_downs = (False, True)
        downs = (None, False, True)

        for init_down, down in it.product(init_downs, downs):
            with self.subTest(init_down=init_down, down=down):

                t = turtle.Turtle(self.sprite, down=init_down)

                self.assertIs(t.down, init_down)

                coro = t.async_move(42, 24, down=down)
                self._run_coroutines(coro)

                self.assertIs(t.down, init_down)

                effective_down = down if down is not None else init_down
                expected_cb = t._async_draw_line if effective_down else None

                self.sprite.async_move.assert_awaited_with(
                    42, 24,
                    callback=expected_cb,
                    speed=None,
                    easing=None,
                    fps=None,
                    update=None,
                )


    def test_async_move_to_awaits_sprite_async_move_to(self):

        t = turtle.Turtle(self.sprite)

        coro = t.async_move_to(42, 24)
        self._run_coroutines(coro)

        self.sprite.async_move_to.assert_awaited_with(
            42, 24,
            callback=t._async_draw_line,
            speed=None,
            easing=None,
            fps=None,
            update=None,
        )


    def test_async_move_to_with_args_awaits_sprite_async_move_to_with_args(self):

        t = turtle.Turtle(self.sprite)

        coro = t.async_move_to(
            42, 24,
            speed='speed',
            easing='easing',
            fps='fps',
            update='update',
        )
        self._run_coroutines(coro)

        self.sprite.async_move_to.assert_awaited_with(
            42, 24,
            callback=t._async_draw_line,
            speed='speed',
            easing='easing',
            fps='fps',
            update='update',
        )


    def test_async_move_to_down_draw_line_vs_init_down(self):

        init_downs = (False, True)
        downs = (None, False, True)

        for init_down, down in it.product(init_downs, downs):
            with self.subTest(init_down=init_down, down=down):

                t = turtle.Turtle(self.sprite, down=init_down)

                self.assertIs(t.down, init_down)

                coro = t.async_move_to(42, 24, down=down)
                self._run_coroutines(coro)

                self.assertIs(t.down, init_down)

                effective_down = down if down is not None else init_down
                expected_cb = t._async_draw_line if effective_down else None

                self.sprite.async_move_to.assert_awaited_with(
                    42, 24,
                    callback=expected_cb,
                    speed=None,
                    easing=None,
                    fps=None,
                    update=None,
                )



class TestTurtleSyncRotation(base.TestCase):

    def setUp(self):

        self.canvas = fake_tkinter.FakeCanvas()
        self.sprite = fake_sprite.FakeSprite(
            canvas=self.canvas,
            anchor=(0, 0),
            angle=0,
        )
        self.t = turtle.Turtle(self.sprite)


    def test_sync_left_calls_sprite_sync_rotate(self):

        self.t.sync_left(90)

        self.sprite.sync_rotate.assert_called_with(
            -90,
            speed=None,
            easing=None,
            fps=None,
            update=None,
        )


    def test_sync_left_with_args_calls_sprite_sync_rotate_with_args(self):

        self.t.sync_left(
            90,
            speed='speed',
            easing='easing',
            fps='fps',
            update='update',
        )

        self.sprite.sync_rotate.assert_called_with(
            -90,
            speed='speed',
            easing='easing',
            fps='fps',
            update='update',
        )


    def test_sync_right_calls_sprite_sync_rotate(self):

        self.t.sync_right(90)

        self.sprite.sync_rotate.assert_called_with(
            90,
            speed=None,
            easing=None,
            fps=None,
            update=None,
        )


    def test_sync_right_with_args_calls_sprite_sync_rotate_with_args(self):

        self.t.sync_right(
            90,
            speed='speed',
            easing='easing',
            fps='fps',
            update='update',
        )

        self.sprite.sync_rotate.assert_called_with(
            90,
            speed='speed',
            easing='easing',
            fps='fps',
            update='update',
        )



class TestTurtleSyncMovement(base.TestCase):

    def setUp(self):

        self.canvas = fake_tkinter.FakeCanvas()
        self.sprite = fake_sprite.FakeSprite(
            canvas=self.canvas,
            anchor=(0, 0),
            angle=0,
        )


    def test_sync_forward_calls_sprite_sync_forward(self):

        t = turtle.Turtle(self.sprite)

        t.sync_forward(42)

        self.sprite.sync_forward.assert_called_with(
            42,
            callback=t._sync_draw_line,
            speed=None,
            easing=None,
            fps=None,
            update=None,
        )


    def test_sync_forward_with_args_calls_sprite_sync_forward_with_args(self):

        t = turtle.Turtle(self.sprite)

        t.sync_forward(
            42,
            speed='speed',
            easing='easing',
            fps='fps',
            update='update',
        )

        self.sprite.sync_forward.assert_called_with(
            42,
            callback=t._sync_draw_line,
            speed='speed',
            easing='easing',
            fps='fps',
            update='update',
        )


    def test_sync_forward_down_draw_line_vs_init_down(self):

        init_downs = (False, True)
        downs = (None, False, True)

        for init_down, down in it.product(init_downs, downs):
            with self.subTest(init_down=init_down, down=down):

                t = turtle.Turtle(self.sprite, down=init_down)

                self.assertIs(t.down, init_down)

                t.sync_forward(42, down=down)

                self.assertIs(t.down, init_down)

                effective_down = down if down is not None else init_down
                expected_cb = t._sync_draw_line if effective_down else None

                self.sprite.sync_forward.assert_called_with(
                    42,
                    callback=expected_cb,
                    speed=None,
                    easing=None,
                    fps=None,
                    update=None,
                )


    def test_sync_backward_calls_sprite_sync_forward(self):

        t = turtle.Turtle(self.sprite)

        t.sync_backward(42)

        self.sprite.sync_forward.assert_called_with(
            -42,
            callback=t._sync_draw_line,
            speed=None,
            easing=None,
            fps=None,
            update=None,
        )


    def test_sync_backward_with_args_calls_sprite_sync_forward_with_args(self):

        t = turtle.Turtle(self.sprite)

        t.sync_backward(
            -42,
            speed='speed',
            easing='easing',
            fps='fps',
            update='update',
        )

        self.sprite.sync_forward.assert_called_with(
            42,
            callback=t._sync_draw_line,
            speed='speed',
            easing='easing',
            fps='fps',
            update='update',
        )


    def test_sync_backward_down_draw_line_vs_init_down(self):

        init_downs = (False, True)
        downs = (None, False, True)

        for init_down, down in it.product(init_downs, downs):
            with self.subTest(init_down=init_down, down=down):

                t = turtle.Turtle(self.sprite, down=init_down)

                self.assertIs(t.down, init_down)

                t.sync_backward(42, down=down)

                self.assertIs(t.down, init_down)

                effective_down = down if down is not None else init_down
                expected_cb = t._sync_draw_line if effective_down else None

                self.sprite.sync_forward.assert_called_with(
                    -42,
                    callback=expected_cb,
                    speed=None,
                    easing=None,
                    fps=None,
                    update=None,
                )


    def test_sync_move_calls_sprite_sync_move(self):

        t = turtle.Turtle(self.sprite)

        t.sync_move(42, 24)

        self.sprite.sync_move.assert_called_with(
            42, 24,
            callback=t._sync_draw_line,
            speed=None,
            easing=None,
            fps=None,
            update=None,
        )


    def test_sync_move_with_args_calls_sprite_sync_move_with_args(self):

        t = turtle.Turtle(self.sprite)

        t.sync_move(
            42, 24,
            speed='speed',
            easing='easing',
            fps='fps',
            update='update',
        )

        self.sprite.sync_move.assert_called_with(
            42, 24,
            callback=t._sync_draw_line,
            speed='speed',
            easing='easing',
            fps='fps',
            update='update',
        )


    def test_sync_move_down_draw_line_vs_init_down(self):

        init_downs = (False, True)
        downs = (None, False, True)

        for init_down, down in it.product(init_downs, downs):
            with self.subTest(init_down=init_down, down=down):

                t = turtle.Turtle(self.sprite, down=init_down)

                self.assertIs(t.down, init_down)

                t.sync_move(42, 24, down=down)

                self.assertIs(t.down, init_down)

                effective_down = down if down is not None else init_down
                expected_cb = t._sync_draw_line if effective_down else None

                self.sprite.sync_move.assert_called_with(
                    42, 24,
                    callback=expected_cb,
                    speed=None,
                    easing=None,
                    fps=None,
                    update=None,
                )


    def test_sync_move_to_calls_sprite_sync_move_to(self):

        t = turtle.Turtle(self.sprite)

        t.sync_move_to(42, 24)

        self.sprite.sync_move_to.assert_called_with(
            42, 24,
            callback=t._sync_draw_line,
            speed=None,
            easing=None,
            fps=None,
            update=None,
        )


    def test_sync_move_to_with_args_calls_sprite_sync_move_to_with_args(self):

        t = turtle.Turtle(self.sprite)

        t.sync_move_to(
            42, 24,
            speed='speed',
            easing='easing',
            fps='fps',
            update='update',
        )

        self.sprite.sync_move_to.assert_called_with(
            42, 24,
            callback=t._sync_draw_line,
            speed='speed',
            easing='easing',
            fps='fps',
            update='update',
        )


    def test_sync_move_to_down_draw_line_vs_init_down(self):

        init_downs = (False, True)
        downs = (None, False, True)

        for init_down, down in it.product(init_downs, downs):
            with self.subTest(init_down=init_down, down=down):

                t = turtle.Turtle(self.sprite, down=init_down)

                self.assertIs(t.down, init_down)

                t.sync_move_to(42, 24, down=down)

                self.assertIs(t.down, init_down)

                effective_down = down if down is not None else init_down
                expected_cb = t._sync_draw_line if effective_down else None

                self.sprite.sync_move_to.assert_called_with(
                    42, 24,
                    callback=expected_cb,
                    speed=None,
                    easing=None,
                    fps=None,
                    update=None,
                )



class TestTurtleAsyncMovementIntegrated(AsyncAnimationBase):

    def setUp(self):

        super().setUp()

        self.canvas = fake_tkinter.FakeCanvas()
        self.sprite = sprite_base.Sprite(self.canvas, shape=None)


    def test_async_forward_draws_calls_canvas_create_line(self):

        t = turtle.Turtle(self.sprite, line_color='pink', line_width=5)

        coro = t.async_forward(100)
        self._run_coroutines(coro)

        self.canvas.create_line.assert_called_with(
            0, 0,
            mock.ANY, 0,
            fill='pink',
            width=5,
            capstyle=mock.ANY,
        )


    def test_async_forward_lines_are_behind_the_sprite(self):

        t = turtle.Turtle(self.sprite)

        coro = t.async_forward(100)
        self._run_coroutines(coro)

        self.canvas.tag_lower.assert_called_with(
            42,     # line canvas id from fake canvas.create_line
            None,   # sprite canvas id, None in the Sprite base class
        )


    def test_async_forward_lines_are_progressively_updated(self):

        t = turtle.Turtle(self.sprite)

        coro = t.async_forward(100, speed=100, fps=10)
        self._run_coroutines(coro)

        # distance=speed=100 and fps=10
        # First frame creates the line, other 9 frames update it.

        coords_call_args_list = self.canvas.coords.call_args_list
        self.assertEqual(
            len(coords_call_args_list),
            9,
            msg='canvas.coords number of calls',
        )

        # All canvas.coords calls include the correct line id: 42
        for call_args in coords_call_args_list:
            self.assertEqual(
                call_args,
                mock.call(42, mock.ANY, mock.ANY, mock.ANY, mock.ANY),
            )


    def test_async_backward_draws_calls_canvas_create_line(self):

        t = turtle.Turtle(self.sprite, line_color='pink', line_width=5)

        coro = t.async_backward(100)
        self._run_coroutines(coro)

        self.canvas.create_line.assert_called_with(
            0, 0,
            mock.ANY, 0,
            fill='pink',
            width=5,
            capstyle=mock.ANY,
        )


    def test_async_backward_lines_are_behind_the_sprite(self):

        t = turtle.Turtle(self.sprite)

        coro = t.async_backward(100)
        self._run_coroutines(coro)

        self.canvas.tag_lower.assert_called_with(
            42,     # line canvas id from fake canvas.create_line
            None,   # sprite canvas id, None in the Sprite base class
        )


    def test_async_backward_lines_are_progressively_updated(self):

        t = turtle.Turtle(self.sprite)

        coro = t.async_backward(100, speed=100, fps=10)
        self._run_coroutines(coro)

        # distance=speed=100 and fps=10
        # First frame creates the line, other 9 frames update it.

        coords_call_args_list = self.canvas.coords.call_args_list
        self.assertEqual(
            len(coords_call_args_list),
            9,
            msg='canvas.coords number of calls',
        )

        # All canvas.coords calls include the correct line id: 42
        for call_args in coords_call_args_list:
            self.assertEqual(
                call_args,
                mock.call(42, mock.ANY, mock.ANY, mock.ANY, mock.ANY),
            )


    def test_async_move_draws_calls_canvas_create_line(self):

        t = turtle.Turtle(self.sprite, line_color='pink', line_width=5)

        coro = t.async_move(40, 30)
        self._run_coroutines(coro)

        self.canvas.create_line.assert_called_with(
            0, 0,
            mock.ANY, mock.ANY,
            fill='pink',
            width=5,
            capstyle=mock.ANY,
        )


    def test_async_move_lines_are_behind_the_sprite(self):

        t = turtle.Turtle(self.sprite)

        coro = t.async_move(40, 30)
        self._run_coroutines(coro)

        self.canvas.tag_lower.assert_called_with(
            42,     # line canvas id from fake canvas.create_line
            None,   # sprite canvas id, None in the Sprite base class
        )


    def test_async_move_lines_are_progressively_updated(self):

        t = turtle.Turtle(self.sprite)

        coro = t.async_move(40, 30, speed=50, fps=10)
        self._run_coroutines(coro)

        # distance=speed=50 and fps=10
        # First frame creates the line, other 9 frames update it.

        coords_call_args_list = self.canvas.coords.call_args_list
        self.assertEqual(
            len(coords_call_args_list),
            9,
            msg='canvas.coords number of calls',
        )

        # All canvas.coords calls include the correct line id: 42
        for call_args in coords_call_args_list:
            self.assertEqual(
                call_args,
                mock.call(42, mock.ANY, mock.ANY, mock.ANY, mock.ANY),
            )


    def test_async_move_to_draws_calls_canvas_create_line(self):

        t = turtle.Turtle(self.sprite, line_color='pink', line_width=5)

        coro = t.async_move_to(40, 30)
        self._run_coroutines(coro)

        self.canvas.create_line.assert_called_with(
            0, 0,
            mock.ANY, mock.ANY,
            fill='pink',
            width=5,
            capstyle=mock.ANY,
        )


    def test_async_move_to_lines_are_behind_the_sprite(self):

        t = turtle.Turtle(self.sprite)

        coro = t.async_move_to(40, 30)
        self._run_coroutines(coro)

        self.canvas.tag_lower.assert_called_with(
            42,     # line canvas id from fake canvas.create_line
            None,   # sprite canvas id, None in the Sprite base class
        )


    def test_async_move_to_lines_are_progressively_updated(self):

        t = turtle.Turtle(self.sprite)

        coro = t.async_move_to(40, 30, speed=50, fps=10)
        self._run_coroutines(coro)

        # distance=speed=50 and fps=10
        # First frame creates the line, other 9 frames update it.

        coords_call_args_list = self.canvas.coords.call_args_list
        self.assertEqual(
            len(coords_call_args_list),
            9,
            msg='canvas.coords number of calls',
        )

        # All canvas.coords calls include the correct line id: 42
        for call_args in coords_call_args_list:
            self.assertEqual(
                call_args,
                mock.call(42, mock.ANY, mock.ANY, mock.ANY, mock.ANY),
            )



