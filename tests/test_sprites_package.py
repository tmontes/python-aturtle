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
from aturtle.shapes import bitmap, vector



class TestFullyPatched(unittest.TestCase):

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
            mock.patch('aturtle.sprites.VectorSprite', self.vector_sprite_mock),

        )
        for patch in patches:
            self.exit_stack.enter_context(patch)


    def tearDown(self):

        self.exit_stack.close()


    def test_create_sprite_from_str(self):

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


    def test_create_sprite_from_path(self):

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


    def test_create_sprite_from_bytes(self):

        canvas = object()
        shape = object()
        self.bitmap_shape_mock.return_value = shape

        _sprite = sprites.create_sprite(canvas, b'image-payload')

        # One shape was created with filename keyword argument.
        self.bitmap_shape_mock.assert_called_once_with(data=b'image-payload')

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


    def test_create_sprite_from_list(self):

        canvas = object()
        shape = object()
        self.vector_shape_mock.return_value = shape

        the_list = [1, 2, 3, 4]
        _sprite = sprites.create_sprite(canvas, the_list)

        # One shape was created with filename keyword argument.
        self.vector_shape_mock.assert_called_once_with(the_list)

        # Sprite created once.
        self.vector_sprite_mock.assert_called_once()

        # Positional arguments are the canvas, and created shape.
        self.assertEqual(
            self.vector_sprite_mock.call_args.args,
            (canvas, shape),
        )

        # Keyword arguments are the default anchor and angle.
        self.assertEqual(
            self.vector_sprite_mock.call_args.kwargs,
            dict(anchor=(0, 0), angle=0),
        )



class TestPartiallyPatched(unittest.TestCase):

    def setUp(self):

        self.bitmap_sprite_mock = mock.Mock()
        self.vector_sprite_mock = mock.Mock()

        self.exit_stack = contextlib.ExitStack()

        patches = (
            mock.patch('aturtle.sprites.BitmapSprite', self.bitmap_sprite_mock),
            mock.patch('aturtle.sprites.VectorSprite', self.vector_sprite_mock),

        )
        for patch in patches:
            self.exit_stack.enter_context(patch)


    def tearDown(self):

        self.exit_stack.close()


    def test_create_sprite_from_vector_shape(self):

        canvas = object()
        shape = vector.Shape([1, 2, 3, 4])

        _sprite = sprites.create_sprite(canvas, shape)

        # Sprite created once.
        self.vector_sprite_mock.assert_called_once()

        # Positional arguments are the canvas, and created shape.
        self.assertEqual(
            self.vector_sprite_mock.call_args.args,
            (canvas, shape),
        )

        # Keyword arguments are the default anchor and angle.
        self.assertEqual(
            self.vector_sprite_mock.call_args.kwargs,
            dict(anchor=(0, 0), angle=0),
        )


    def test_create_sprite_from_bitmap_shape(self):

        canvas = object()

        class TestBitmapShape(bitmap.Shape):
            def __init__(self):
                pass

        shape = TestBitmapShape()

        _sprite = sprites.create_sprite(canvas, shape)

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



class TestNonPatched(unittest.TestCase):

    def test_create_sprite_with_unsupported_type_raises_TypeError(self):

        canvas = object()

        bad_typed_shape_sources = (
            bool(),
            int(),
            float(),
            tuple(),
            dict(),
            range(42),
            (i for i in 'a-generator-object'),
        )

        for bad_shape_source in bad_typed_shape_sources:
            with self.subTest(bad_shape_source=bad_shape_source):
                with self.assertRaises(TypeError):
                    _sprite = sprites.create_sprite(canvas, bad_shape_source)
