# ----------------------------------------------------------------------------
# Python A-Turtle
# ----------------------------------------------------------------------------
# Copyright (c) Tiago Montes.
# See LICENSE for details.
# ----------------------------------------------------------------------------

import contextlib
import unittest
from unittest import mock

from aturtle import canvas

from . import fake_tkinter



SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480


class TestInvertedTkYCanvas(unittest.TestCase):

    def setUp(self):

        self.tkinter = fake_tkinter.FakeTkinter(
            screen_width=SCREEN_WIDTH,
            screen_height=SCREEN_HEIGHT,
        )
        self.master = self.tkinter.Tk()

        self._exit_stack = contextlib.ExitStack()
        self._exit_stack.enter_context(
            mock.patch('aturtle.canvas.tkinter', self.tkinter)
        )


    def tearDown(self):

        self._exit_stack.close()


    def test_create_creates_tkinter_Canvas(self):

        _c = canvas.InvertedYCanvas(self.master, 'background')

        self.assertEqual(len(self.tkinter.canvases), 1, 'tkinter.Canvas call count')


    def test_create_creates_tkinter_Canvas_with_given_master(self):

        _c = canvas.InvertedYCanvas(self.master, 'background')

        canvas_init_args = self.tkinter.canvases[0].init_args

        # Passed a single positional argument: self.master
        self.assertIs(canvas_init_args.args[0], self.master)


    def test_create_creates_tkinter_Canvas_with_given_background(self):

        _c = canvas.InvertedYCanvas(self.master, 'background')

        canvas_init_args = self.tkinter.canvases[0].init_args
        self.assertEqual(canvas_init_args.kwargs['background'], 'background')


    def test_create_creates_tkinter_Canvas_with_zero_highlightthickness(self):

        _c = canvas.InvertedYCanvas(self.master, 'background')

        canvas_init_args = self.tkinter.canvases[0].init_args
        self.assertEqual(canvas_init_args.kwargs['highlightthickness'], 0)


    def test_create_polygon_returns_integer_item_id(self):

        c = canvas.InvertedYCanvas(self.master, None)

        item_id = c.create_polygon([], fill='fill', outline='outline', width=42)

        self.assertIsInstance(item_id, int)


    def test_create_polygon_inverts_y_coordinates(self):

        c = canvas.InvertedYCanvas(self.master, None)

        coords = [0, 0, 1, 1, 2, -2]
        _item_id = c.create_polygon(coords, fill='fill', outline='outline', width=42)

        wrapped_tkinter_canvas = self.tkinter.canvases[0]
        wrapped_tkinter_canvas.create_polygon.assert_called_once_with(
            [0, 0, 1, -1, 2, 2],
            fill=mock.ANY,
            outline=mock.ANY,
            width=mock.ANY,
        )


    def test_create_polygon_passes_args_to_Canvas_create_polygon(self):

        c = canvas.InvertedYCanvas(self.master, None)

        _item_id = c.create_polygon([], fill='fill', outline='outline', width=42)

        wrapped_tkinter_canvas = self.tkinter.canvases[0]
        wrapped_tkinter_canvas.create_polygon.assert_called_once_with(
            mock.ANY,
            fill='fill',
            outline='outline',
            width=42,
        )


    def test_create_image_returns_integer_item_id(self):

        c = canvas.InvertedYCanvas(self.master, None)

        item_id = c.create_image(0, 0, image=None, anchor=None)

        self.assertIsInstance(item_id, int)


    def test_create_image_inverts_y_coordinate(self):

        c = canvas.InvertedYCanvas(self.master, None)

        _item_id = c.create_image(42, 24, image=None, anchor=None)

        wrapped_tkinter_canvas = self.tkinter.canvases[0]
        wrapped_tkinter_canvas.create_image.assert_called_with(
            42, -24, image=mock.ANY, anchor=mock.ANY
        )


    def test_create_image_passes_args_to_Canvas_create_image(self):

        c = canvas.InvertedYCanvas(self.master, None)

        _item_id = c.create_image(42, 24, image='image', anchor='anchor')

        wrapped_tkinter_canvas = self.tkinter.canvases[0]
        wrapped_tkinter_canvas.create_image.assert_called_with(
            mock.ANY, mock.ANY, image='image', anchor='anchor'
        )


    def test_create_line_returns_integer_item_id(self):

        c = canvas.InvertedYCanvas(self.master, None)

        item_id = c.create_line([], fill='fill', width=42, capstyle='capstyle')

        self.assertIsInstance(item_id, int)


    def test_create_line_inverts_y_coordinates(self):

        c = canvas.InvertedYCanvas(self.master, None)

        coords = [0, 0, 1, 1, 2, -2]
        _item_id = c.create_line(coords, fill='fill', width=42, capstyle='capstyle')

        wrapped_tkinter_canvas = self.tkinter.canvases[0]
        wrapped_tkinter_canvas.create_line.assert_called_with(
            [0, 0, 1, -1, 2, 2], fill=mock.ANY, width=mock.ANY, capstyle=mock.ANY,
        )


    def test_create_line_passes_args_to_Canvas_create_line(self):

        c = canvas.InvertedYCanvas(self.master, None)

        _item_id = c.create_line([], fill='fill', width=42, capstyle='capstyle')

        wrapped_tkinter_canvas = self.tkinter.canvases[0]
        wrapped_tkinter_canvas.create_line.assert_called_with(
            mock.ANY, fill='fill', width=42, capstyle='capstyle',
        )


    def test_move_calls_canvas_move_with_same_item_id(self):

        c = canvas.InvertedYCanvas(self.master, None)

        c.move(42, 0, 0)

        wrapped_tkinter_canvas = self.tkinter.canvases[0]
        wrapped_tkinter_canvas.move.assert_called_with(42, mock.ANY, mock.ANY)


    def test_move_calls_canvas_move_with_inverted_y(self):

        c = canvas.InvertedYCanvas(self.master, None)

        c.move(None, 42, 24)

        wrapped_tkinter_canvas = self.tkinter.canvases[0]
        wrapped_tkinter_canvas.move.assert_called_with(mock.ANY, 42, -24)


    def test_coords_calls_canvas_coords_with_same_item_id(self):

        c = canvas.InvertedYCanvas(self.master, None)

        c.coords(42, [])

        wrapped_tkinter_canvas = self.tkinter.canvases[0]
        wrapped_tkinter_canvas.coords.assert_called_with(42, mock.ANY)


    def test_coords_calls_canvas_coords_with_inverted_y_coords(self):

        c = canvas.InvertedYCanvas(self.master, None)

        c.coords(None, [1, 2, 3, 4, 5, 6])

        wrapped_tkinter_canvas = self.tkinter.canvases[0]
        wrapped_tkinter_canvas.coords.assert_called_with(
            mock.ANY, [1, -2, 3, -4, 5, -6]
        )


    def test_attribute_access_returns_tkinter_Canvas_attribute(self):

        c = canvas.InvertedYCanvas(self.master, None)

        names = (
            'pack',
            'config',
            'xview_scroll',
            'yview_scroll',
            'update',
            'delete',
            'itemconfig',
            'tag_lower',
            'tag_raise',
        )

        wrapped_tkinter_canvas = self.tkinter.canvases[0]
        for name in names:
            with self.subTest(attr_name=name):
                result = getattr(c, name)
                underlying = getattr(wrapped_tkinter_canvas, name)
                self.assertIs(result, underlying)
