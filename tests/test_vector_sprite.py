# ----------------------------------------------------------------------------
# Python A-Turtle
# ----------------------------------------------------------------------------
# Copyright (c) Tiago Montes.
# See LICENSE for details.
# ----------------------------------------------------------------------------

import math
import unittest

from aturtle import sprites, shapes

from . import fake_tkinter


class UnitSquare(shapes.vector.Square):

    def __init__(self, fill_color=None, line_color=None, line_width=None):

        super().__init__(
            side=1,
            fill_color=fill_color,
            line_color=line_color,
            line_width=line_width,
        )


class TestVectorSprite(unittest.TestCase):

    def setUp(self):

        self.canvas = fake_tkinter.FakeCanvas()


    def test_create(self):

        s = sprites.VectorSprite(self.canvas, UnitSquare())


    def test_default_x_anchor(self):

        s = sprites.VectorSprite(self.canvas, UnitSquare())
        self.assertEqual(s.x, 0)


    def test_default_y_anchor(self):

        s = sprites.VectorSprite(self.canvas, UnitSquare())
        self.assertEqual(s.y, 0)


    def test_shape_fill_color_passed_to_create_polygon(self):

        s = sprites.VectorSprite(self.canvas, UnitSquare(fill_color='#009fff'))

        create_polygon_kwargs = self.canvas._polygon_kwargs
        self.assertEqual(create_polygon_kwargs['fill'], '#009fff')


    def test_shape_line_color_passed_to_create_polygon(self):

        s = sprites.VectorSprite(self.canvas, UnitSquare(line_color='black'))

        create_polygon_kwargs = self.canvas._polygon_kwargs
        self.assertEqual(create_polygon_kwargs['outline'], 'black')


    def test_shape_line_width_passed_to_create_polygon(self):

        s = sprites.VectorSprite(self.canvas, UnitSquare(line_width=2))

        create_polygon_kwargs = self.canvas._polygon_kwargs
        self.assertEqual(create_polygon_kwargs['width'], 2)


    def test_create_custom_anchor_x(self):

        s = sprites.VectorSprite(self.canvas, UnitSquare(), anchor=(2, 1))
        self.assertEqual(s.x, 2)


    def test_create_custom_anchor_y(self):

        s = sprites.VectorSprite(self.canvas, UnitSquare(), anchor=(2, 1))
        self.assertEqual(s.y, 1)


    def test_create_custom_anchor_coords(self):

        s = sprites.VectorSprite(self.canvas, UnitSquare(), anchor=(2, 1))

        shape_coords_after_offset = [2.5, 0.5, 2.5, 1.5, 1.5, 1.5, 1.5, 0.5]
        self.assertEqual(s.coords, shape_coords_after_offset)


    def test_horizontal_move_moves_anchor_x(self):

        s = sprites.VectorSprite(self.canvas, UnitSquare())
        s.move(20, 0)
        self.assertEqual(s.x, 20)


    def test_vertical_move_moves_anchor_y(self):

        s = sprites.VectorSprite(self.canvas, UnitSquare())
        s.move(0, 10)
        self.assertEqual(s.y, 10)


    def test_move_does_not_call_canvas_update(self):

        s = sprites.VectorSprite(self.canvas, UnitSquare())
        s.move(0, 10)
        self.canvas.update.assert_not_called()


    def test_move_with_update_calls_calls_canvas_update(self):

        s = sprites.VectorSprite(self.canvas, UnitSquare())
        s.move(0, 10, update=True)
        self.canvas.update.assert_called_once_with()


    def test_horizontal_moveto_moves_anchor_x(self):

        s = sprites.VectorSprite(self.canvas, UnitSquare())
        s.moveto(20, 0)
        self.assertEqual(s.x, 20)


    def test_vertical_moveto_moves_anchor_y(self):

        s = sprites.VectorSprite(self.canvas, UnitSquare())
        s.moveto(0, 10)
        self.assertEqual(s.y, 10)


    def test_moveto_does_not_call_canvas_update(self):

        s = sprites.VectorSprite(self.canvas, UnitSquare())
        s.moveto(0, 10)
        self.canvas.update.assert_not_called()


    def test_moveto_with_update_calls_calls_canvas_update(self):

        s = sprites.VectorSprite(self.canvas, UnitSquare())
        s.moveto(0, 10, update=True)
        self.canvas.update.assert_called_once_with()


    def test_rotate_does_not_change_anchor_x(self):

        s = sprites.VectorSprite(self.canvas, UnitSquare())
        original_x = s.x

        s.rotate(1)
        self.assertEqual(original_x, s.x)


    def test_rotate_does_not_change_anchor_y(self):

        s = sprites.VectorSprite(self.canvas, UnitSquare())
        original_y = s.y

        s.rotate(1)
        self.assertEqual(original_y, s.y)


    def test_rotate_updates_coords(self):

        s = sprites.VectorSprite(self.canvas, UnitSquare())
        original_coords = list(s.coords)

        s.rotate(180)
        # Half-circle rotated coords are easy to determine.
        expected_coords = original_coords[4:] + original_coords[:5]
        for orig, new in zip(expected_coords, s.coords):
            self.assertAlmostEqual(orig, new, places=5)


    def test_rotate_around_point_rotates_anchor_x(self):

        s = sprites.VectorSprite(self.canvas, UnitSquare())

        s.rotate(180, around=(1, 1))
        self.assertAlmostEqual(s.x, 2, places=5)


    def test_rotate_around_point_rotates_anchor_y(self):

        s = sprites.VectorSprite(self.canvas, UnitSquare())

        s.rotate(180, around=(1, 1))
        self.assertAlmostEqual(s.y, 2, places=5)


    def test_rotate_around_point_updates_coords(self):

        s = sprites.VectorSprite(self.canvas, UnitSquare())

        s.rotate(180, around=(1, 1))
        # Half-circle rotated coords around (1, 1) are these.
        expected_coords = [1.5, 2.5, 1.5, 1.5, 2.5, 1.5, 2.5, 2.5]
        for orig, new in zip(expected_coords, s.coords):
            self.assertAlmostEqual(orig, new, places=5)


    def test_rotate_does_not_call_canvas_update(self):

        s = sprites.VectorSprite(self.canvas, UnitSquare())
        s.rotate(1)
        self.canvas.update.assert_not_called()


    def test_rotate_with_update_calls_calls_canvas_update(self):

        s = sprites.VectorSprite(self.canvas, UnitSquare())
        s.rotate(1, update=True)
        self.canvas.update.assert_called_once_with()


    def test_unrotate_does_not_change_anchor_x(self):

        s = sprites.VectorSprite(self.canvas, UnitSquare())
        original_x = s.x

        s.unrotate()
        self.assertEqual(original_x, s.x)


    def test_unrotate_does_not_change_anchor_y(self):

        s = sprites.VectorSprite(self.canvas, UnitSquare())
        original_y = s.y

        s.unrotate()
        self.assertEqual(original_y, s.y)


    def test_unrotate_does_not_call_canvas_update(self):

        s = sprites.VectorSprite(self.canvas, UnitSquare())
        s.unrotate()
        self.canvas.update.assert_not_called()


    def test_unrotate_with_update_calls_calls_canvas_update(self):

        s = sprites.VectorSprite(self.canvas, UnitSquare())
        s.unrotate(update=True)
        self.canvas.update.assert_called_once_with()


    def test_update_calls_canvas_update(self):

        s = sprites.VectorSprite(self.canvas, UnitSquare())

        s.update()
        self.canvas.update.assert_called_once_with()


    def test_delete_calls_canvas_delete(self):

        s = sprites.VectorSprite(self.canvas, UnitSquare())

        s.delete()
        self.canvas.delete.assert_called_once()


    def test_two_deletes_only_call_canvas_delete_once(self):

        s = sprites.VectorSprite(self.canvas, UnitSquare())

        s.delete()
        s.delete()
        self.canvas.delete.assert_called_once()
