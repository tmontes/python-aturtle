# ----------------------------------------------------------------------------
# Python A-Turtle
# ----------------------------------------------------------------------------
# Copyright (c) Tiago Montes.
# See LICENSE for details.
# ----------------------------------------------------------------------------

import contextlib
import pathlib
import unittest
from unittest import mock

from aturtle import sprites



class Test(unittest.TestCase):

    def setUp(self):

        self.bitmap_shape_mock = mock.Mock()
        self.vector_shape_mock = mock.Mock()
        self.bitmap_sprite_mock = mock.Mock()
        self.vector_sprite_mock = mock.Mock()

        self.exit_stack = contextlib.ExitStack()

        patches = (
            mock.patch('aturtle.sprites._BitmapShape', self.bitmap_shape_mock),
            mock.patch('aturtle.sprites._VectorShape', self.vector_shape_mock),
            mock.patch('aturtle.sprites.BitmapSprite', self.bitmap_sprite_mock),
            mock.patch('aturtle.sprites.BitmapSprite', self.bitmap_sprite_mock),

        )
        for patch in patches:
            self.exit_stack.enter_context(patch)


    def tearDown(self):

        self.exit_stack.close()


    def test_create_sprite_from_str_loads_bitmap_filename(self):

        canvas = object()
        shape = object()
        self.bitmap_shape_mock.return_value = shape

        _sprite = sprites.create_sprite(canvas, 'filename')

        # One shape was created with filename keyword argument.
        self.bitmap_shape_mock.assert_called_once_with(filename='filename')

        # Sprite created once.
        self.bitmap_sprite_mock.assert_called_once()

        # Positional arguments are the canvas, and created shape.
        self.assertEqual(
            self.bitmap_sprite_mock.call_args.args,
            (canvas, shape),
        )

        # Keyword arguments are the default anchor and angle.
        self.assertEqual(
            self.bitmap_sprite_mock.call_args.kwargs,
            dict(anchor=(0, 0), angle=0),
        )


    def test_create_sprite_from_path_loads_bitmap_filename(self):

        canvas = object()
        shape = object()
        self.bitmap_shape_mock.return_value = shape

        path = pathlib.Path()

        _sprite = sprites.create_sprite(canvas, path)

        # One shape was created with filename keyword argument.
        self.bitmap_shape_mock.assert_called_once_with(filename=path)

        # Sprite created once.
        self.bitmap_sprite_mock.assert_called_once()

        # Positional arguments are the canvas, and created shape.
        self.assertEqual(
            self.bitmap_sprite_mock.call_args.args,
            (canvas, shape),
        )

        # Keyword arguments are the default anchor and angle.
        self.assertEqual(
            self.bitmap_sprite_mock.call_args.kwargs,
            dict(anchor=(0, 0), angle=0),
        )

