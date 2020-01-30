# ----------------------------------------------------------------------------
# Python A-Turtle
# ----------------------------------------------------------------------------
# Copyright (c) Tiago Montes.
# See LICENSE for details.
# ----------------------------------------------------------------------------

import contextlib
import types
import unittest
from unittest import mock

from aturtle import window

from . import fake_tkinter


SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480


class FakedTkinterTestCase(unittest.TestCase):

    def setUp(self):

        self.tkinter = fake_tkinter.FakeTkinter(
            screen_width=SCREEN_WIDTH,
            screen_height=SCREEN_HEIGHT,
        )
        self.exit_stack = contextlib.ExitStack()
        self.exit_stack.enter_context(
            mock.patch('aturtle.window.tkinter', self.tkinter)
        )


    def _Window(self, *args, **kwargs):

        # Default Window canvas is based on tkinter.Canvas. Use fake in tests.

        return window.Window(*args, **kwargs, canvas_factory=self.tkinter.Canvas)


    def tearDown(self):

        self.exit_stack.close()
        self._reset_window_class_state()


    def _reset_window_class_state(self):

        window.Window.close_all(strict=False)



class TestWindow(FakedTkinterTestCase):

    def test_create(self):

        w = self._Window()


    def test_create_window_creates_underlying_tk_object(self):

        w = self._Window()
        self.assertIsInstance(w._tk_window, fake_tkinter.FakeTk)


    def test_default_title_was_set(self):

        w = self._Window()
        tk_window = w._tk_window
        tk_window.title.assert_called_once_with('A-Turtle')


    def test_default_width(self):

        w = self._Window()
        self.assertEqual(w.width, 320)


    def test_default_height(self):

        w = self._Window()
        self.assertEqual(w.height, 320)


    def test_default_x_is_screen_centered(self):

        w = self._Window(width=200)
        self.assertEqual(w.x, (SCREEN_WIDTH - 200) // 2)


    def test_default_y_is_screen_centered(self):

        w = self._Window(height=200)
        self.assertEqual(w.y, (SCREEN_HEIGHT - 200) // 2)


    def test_has_canvas(self):

        w = self._Window()
        self.assertIsNotNone(w.canvas)


    def test_canvas_was_packed(self):

        w = self._Window()
        w.canvas.pack.assert_called_once_with(expand=True, fill='both')


    def test_canvas_default_fill_is_white(self):

        w = self._Window()

        self.assertEqual(len(self.tkinter.canvases), 1, 'Non single canvas init.')

        canvas_init_args = self.tkinter.canvases[0].init_args
        self.assertEqual(canvas_init_args.kwargs['background'], 'white')


    def test_canvas_origin_is_centered(self):

        w = self._Window(width=300, height=200)

        w.canvas.config.assert_called_once_with(
            xscrollincrement=1,
            yscrollincrement=1,
        )
        w.canvas.xview_scroll.assert_called_once_with(-150, 'units')
        w.canvas.yview_scroll.assert_called_once_with(-100, 'units')


    def test_resize_handler_in_place(self):

        w = self._Window()

        tk_window = w._tk_window
        tk_window.bind.assert_called_once()

        (sequence, func), _kwargs = tk_window.bind.call_args
        self.assertEqual(sequence, '<Configure>')
        self.assertTrue(callable(func), 'Resize handler not callable.')


    def test_resize_handler_adjusts_canvas_scroll(self):

        w = self._Window()

        w.canvas.xview_scroll.reset_mock()
        w.canvas.yview_scroll.reset_mock()

        event = types.SimpleNamespace()
        event.width = 200
        event.height = 100
        w._resize_handler(event)

        w.canvas.xview_scroll.assert_called_once()
        w.canvas.yview_scroll.assert_called_once()


    def test_custom_size_width(self):

        w = self._Window(width=200, height=100)
        self.assertEqual(w.width, 200)


    def test_custom_size_height(self):

        w = self._Window(width=200, height=100)
        self.assertEqual(w.height, 100)


    def test_custom_placement_x(self):

        w = self._Window(x=100)
        self.assertEqual(w.x, 100)


    def test_custom_placement_negative_x(self):

        w = self._Window(x=-100)
        self.assertEqual(w.x, SCREEN_WIDTH - w.width - 100)


    def test_custom_placement_y(self):

        w = self._Window(y=50)
        self.assertEqual(w.y, 50)


    def test_custom_placement_negative_y(self):

        w = self._Window(y=-50)
        self.assertEqual(w.y, SCREEN_HEIGHT - w.height - 50)


    def test_custom_fill_passed_to_canvas(self):

        w = self._Window(fill_color='orange')

        self.assertEqual(len(self.tkinter.canvases), 1, 'Non single canvas init.')

        canvas_init_args = self.tkinter.canvases[0].init_args
        self.assertEqual(canvas_init_args.kwargs['background'], 'orange')


    def test_custom_title_passed_to_tk_window(self):

        w = self._Window(title='Test Title')
        tk_window = w._tk_window
        tk_window.title.assert_called_once_with('Test Title')


    def test_positive_horizontal_placement(self):

        w = self._Window()
        w.x = 100
        self.assertEqual(w.x, 100)


    def test_positive_vertical_placement(self):

        w = self._Window()
        w.y = 50
        self.assertEqual(w.y, 50)


    def test_negative_horizontal_placement(self):

        w = self._Window()
        w.x = -100
        self.assertEqual(w.x, SCREEN_WIDTH - w.width - 100)


    def test_negative_vertical_placement(self):

        w = self._Window()
        w.y = -50
        self.assertEqual(w.y, SCREEN_HEIGHT - w.height - 50)


    def test_horizontal_sizing(self):

        w = self._Window()
        w.width = 200
        self.assertEqual(w.width, 200)


    def test_vertical_sizing(self):

        w = self._Window()
        w.height = 100
        self.assertEqual(w.height, 100)


    def test_close(self):

        w = self._Window()
        w.close()


    def test_no_canvas_after_close(self):

        w = self._Window()
        w.close()
        self.assertIsNone(w.canvas)


    def test_close_all(self):

        w = self._Window()
        w.close_all()


    def test_second_close_all_raises(self):

        w = self._Window()
        w.close_all()
        with self.assertRaises(RuntimeError):
            w.close_all()


    def test_no_canvas_after_close_all(self):

        w = self._Window()
        w.close_all()

        self.assertIsNone(w.canvas)



class TestWindowEventHandling(FakedTkinterTestCase):

    def setUp(self):

        super().setUp()
        self.w = self._Window()


    def test_bind_calls_tk_window_bind(self):

        handler = mock.Mock()
        self.w.bind('<KeyPress-a>', handler)

        self.w._tk_window.bind.assert_called_with('<KeyPress-a>', handler)


    def test_bind_unbind_calls_tk_window_bind_unbind(self):

        handler = mock.Mock()
        self.w.bind('<KeyPress-a>', handler)
        self.w.unbind('<KeyPress-a>')

        self.w._tk_window.bind.assert_called_with('<KeyPress-a>', handler)
        self.w._tk_window.unbind.assert_called_with('<KeyPress-a>', mock.ANY)


    def test_unbind_unbound_raises_ValueError(self):

        with self.assertRaises(ValueError):
            self.w.unbind('<KeyPress-a>')


    def test_unbind_default_works_with_no_bindings(self):

        self.w.unbind()
        self.w._tk_window.unbind.assert_not_called()


    def test_unbind_default_unbinds_all_bindings(self):

        self.w.bind('<KeyPress-a>', mock.Mock())
        self.w.bind('<KeyPress-b>', mock.Mock())

        self.w.unbind()
        unbind_call_args = self.w._tk_window.unbind.call_args_list
        self.assertEqual(len(unbind_call_args), 2, 'unbind call count')


    def test_bind_direct_key_with_no_cbs_raises_ValueError(self):

        with self.assertRaises(ValueError):
            self.w.bind_direct_key('a')


    def test_bind_direct_key_with_press_cb_calls_window_bind_twice(self):

        # Ignore any window setup bind calls that may have taken place.
        self.w._tk_window.bind.reset_mock()

        self.w.bind_direct_key('x', mock.Mock())

        bind_call_args = self.w._tk_window.bind.call_args_list
        self.assertEqual(len(bind_call_args), 2, 'unbind call count')

        first_call, second_call = bind_call_args
        self.assertEqual(first_call, mock.call('<KeyPress-x>', mock.ANY))
        self.assertEqual(second_call, mock.call('<KeyRelease-x>', mock.ANY))


    def test_bind_direct_key_with_release_cb_calls_window_bind_twice(self):

        # Ignore any window setup bind calls that may have taken place.
        self.w._tk_window.bind.reset_mock()

        self.w.bind_direct_key('y', None, mock.Mock())

        bind_call_args = self.w._tk_window.bind.call_args_list
        self.assertEqual(len(bind_call_args), 2, 'unbind call count')

        first_call, second_call = bind_call_args
        self.assertEqual(first_call, mock.call('<KeyPress-y>', mock.ANY))
        self.assertEqual(second_call, mock.call('<KeyRelease-y>', mock.ANY))


    def test_bind_direct_key_with_both_cbs_calls_window_bind_twice(self):

        # Ignore any window setup bind calls that may have taken place.
        self.w._tk_window.bind.reset_mock()

        self.w.bind_direct_key('z', mock.Mock(), mock.Mock())

        bind_call_args = self.w._tk_window.bind.call_args_list
        self.assertEqual(len(bind_call_args), 2, 'bind call count')

        first_call, second_call = bind_call_args
        self.assertEqual(first_call, mock.call('<KeyPress-z>', mock.ANY))
        self.assertEqual(second_call, mock.call('<KeyRelease-z>', mock.ANY))


    def test_bind_unbind_direct_key_calls_window_bind_unbind_twice(self):

        # Ignore any window setup bind calls that may have taken place.
        self.w._tk_window.bind.reset_mock()

        self.w.bind_direct_key('a', mock.Mock(), mock.Mock())
        self.w.unbind_direct_key('a')

        bind_call_args = self.w._tk_window.bind.call_args_list
        self.assertEqual(len(bind_call_args), 2, 'bind call count')

        first_call, second_call = bind_call_args
        self.assertEqual(first_call, mock.call('<KeyPress-a>', mock.ANY))
        self.assertEqual(second_call, mock.call('<KeyRelease-a>', mock.ANY))

        unbind_call_args = self.w._tk_window.unbind.call_args_list
        self.assertEqual(len(unbind_call_args), 2, 'unbind call count')

        first_call, second_call = unbind_call_args
        self.assertEqual(first_call, mock.call('<KeyPress-a>', mock.ANY))
        self.assertEqual(second_call, mock.call('<KeyRelease-a>', mock.ANY))


    def test_unbind_direct_key_unknown_raises_ValueError(self):

        with self.assertRaises(ValueError):
            self.w.unbind_direct_key('b')


    def test_unbind_direct_key_default_works_with_no_bindings(self):

        self.w.unbind_direct_key()
        self.w._tk_window.unbind.assert_not_called()


    def test_unbind_direct_key_default_unbinds_all_direct_keys(self):

        self.w.bind_direct_key('a', mock.Mock(), mock.Mock())
        self.w.bind_direct_key('b', mock.Mock(), mock.Mock())

        self.w.unbind_direct_key()

        # Expect 4 unbind calls: KeyPress/KeyRelease for 2 keys.
        unbind_call_args = self.w._tk_window.unbind.call_args_list
        self.assertEqual(len(unbind_call_args), 4, 'unbind call count')


    def _event(self, keysym):

        event = mock.Mock()
        event.keysym = keysym
        return event


    def test_bind_direct_key_press_and_release(self):

        press_cb = mock.Mock()
        release_cb = mock.Mock()
        self.w.bind_direct_key('a', press_cb, release_cb)

        # KeyPress event.
        event = self._event('a')
        self.w._direct_key_press(event)

        # Press callback called.
        press_cb.assert_called_once()
        press_cb.assert_called_with(event)
        release_cb.assert_not_called()

        press_cb.reset_mock()

        # KeyRelease event. Not held down so _direct_key_idle called.
        self.w._direct_key_release(event)
        self.w._direct_key_idle(event)

        # Release callback called.
        press_cb.assert_not_called()
        release_cb.assert_called_once()
        release_cb.assert_called_with(event)


    def test_bind_direct_key_press_hold_and_release(self):

        press_cb = mock.Mock()
        release_cb = mock.Mock()
        self.w.bind_direct_key('a', press_cb, release_cb)

        # KeyPress event.
        event = self._event('a')
        self.w._direct_key_press(event)

        # Press callback called.
        press_cb.assert_called_once()
        press_cb.assert_called_with(event)
        release_cb.assert_not_called()

        press_cb.reset_mock()

        # Holding the key triggers KeyPress/KeyReleases repeatedly.
        # But never idle, so _direct_key_idle never called.
        for _ in range(10):
            self.w._direct_key_release(event)
            self.w._direct_key_press(event)

            # No callbacks while key held down.
            press_cb.assert_not_called()
            release_cb.assert_not_called()

        # Last KeyRelease event. Not held down so _direct_key_idle called.
        self.w._direct_key_release(event)
        self.w._direct_key_idle(event)

        # Release callback called.
        press_cb.assert_not_called()
        release_cb.assert_called_once()
        release_cb.assert_called_with(event)



class TestMultipleWindows(FakedTkinterTestCase):

    def test_create_two_windows(self):

        w1 = self._Window()
        w2 = self._Window()


    def test_close_two_windows(self):

        w1 = self._Window()
        w2 = self._Window()
        w2.close()
        w1.close()


    def test_first_has_underlying_tk_others_have_underlying_toplevels(self):

        w1 = self._Window()
        w2 = self._Window()
        w3 = self._Window()

        self.assertIsInstance(w1._tk_window, fake_tkinter.FakeTk)
        self.assertIsInstance(w2._tk_window, fake_tkinter.FakeToplevel)
        self.assertIsInstance(w3._tk_window, fake_tkinter.FakeToplevel)


    def test_close_first_window_raises_if_there_are_other_windows(self):

        w1 = self._Window()
        w2 = self._Window()

        with self.assertRaises(RuntimeError):
            w1.close()
