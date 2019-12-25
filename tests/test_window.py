# ----------------------------------------------------------------------------
# Python A-Turtle
# ----------------------------------------------------------------------------
# Copyright (c) Tiago Montes.
# See LICENSE for details.
# ----------------------------------------------------------------------------

import contextlib
import unittest
from unittest import mock

from . import fake_tkinter

from aturtle import window


SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480


class TestOneWindow(unittest.TestCase):

    def setUp(self):

        self.tkinter = fake_tkinter.FakeTkinter(
            screen_width=SCREEN_WIDTH,
            screen_height=SCREEN_HEIGHT,
        )
        self.exit_stack = contextlib.ExitStack()
        self.exit_stack.enter_context(
            mock.patch('aturtle.window.tkinter', self.tkinter)
        )


    def tearDown(self):

        self.exit_stack.close()
        self._reset_window_class_state()


    def _reset_window_class_state(self):

        window.Window.close_all(strict=False)


    def test_create(self):

        w = window.Window()


    def test_created_underlying_tk_object(self):

        self.assertEqual(self.tkinter.tk_calls, 0)
        w = window.Window()
        self.assertEqual(self.tkinter.tk_calls, 1)


    def test_default_title_was_set(self):

        w = window.Window()
        tk_window = w._tk_window
        tk_window.title.assert_called_once_with('A-Turtle')


    def test_default_width(self):

        w = window.Window()
        self.assertEqual(w.width, 320)


    def test_default_height(self):

        w = window.Window()
        self.assertEqual(w.height, 320)


    def test_default_x_is_screen_centered(self):

        w = window.Window(width=200)
        self.assertEqual(w.x, (SCREEN_WIDTH - 200) // 2)


    def test_default_y_is_screen_centered(self):

        w = window.Window(height=200)
        self.assertEqual(w.y, (SCREEN_HEIGHT - 200) // 2)


    def test_has_canvas(self):

        w = window.Window()
        self.assertIsNotNone(w.canvas)


    def test_canvas_was_packed(self):

        w = window.Window()
        w.canvas.pack.assert_called_once_with(expand=True, fill='both')


    def test_canvas_border_removed(self):

        w = window.Window()
        fake_canvas = self.tkinter.Canvas
        fake_canvas.assert_called_once()

        (_tk_window,), kwargs = fake_canvas.call_args
        self.assertEqual(kwargs['highlightthickness'], 0)


    def test_canvas_default_fill_is_white(self):

        w = window.Window()
        fake_canvas = self.tkinter.Canvas
        fake_canvas.assert_called_once()

        (_tk_window,), kwargs = fake_canvas.call_args
        self.assertEqual(kwargs['background'], 'white')


    def test_canvas_origin_is_centered(self):

        w = window.Window(width=200, height=200)

        w.canvas.config.assert_called_once_with(
            xscrollincrement=1,
            yscrollincrement=1,
        )
        w.canvas.xview_scroll.assert_called_once_with(-100, 'units')
        w.canvas.yview_scroll.assert_called_once_with(-100, 'units')


    def test_resize_handler_in_place(self):

        w = window.Window()

        tk_window = w._tk_window
        tk_window.bind.assert_called_once()

        (sequence, func), _kwargs = tk_window.bind.call_args
        self.assertEqual(sequence, '<Configure>')
        self.assertTrue(callable(func), 'Resize handler not callable.')


    def test_close(self):

        w = window.Window()
        w.close()


    def test_no_canvas_after_close(self):

        w = window.Window()
        w.close()
        self.assertIsNone(w.canvas)


    def test_close_all(self):

        w = window.Window()
        w.close_all()


    def test_no_canvas_after_close_all(self):

        w = window.Window()
        w.close_all()

        self.assertIsNone(w.canvas)
