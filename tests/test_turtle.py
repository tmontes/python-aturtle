# ----------------------------------------------------------------------------
# Python A-Turtle
# ----------------------------------------------------------------------------
# Copyright (c) Tiago Montes.
# See LICENSE for details.
# ----------------------------------------------------------------------------

import collections
import contextlib
from unittest import mock

from aturtle import turtle

from . import base
from . import fake_tkinter
from . import fake_sprite



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

    pass



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

    pass

