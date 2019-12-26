# ----------------------------------------------------------------------------
# Python A-Turtle
# ----------------------------------------------------------------------------
# Copyright (c) Tiago Montes.
# See LICENSE for details.
# ----------------------------------------------------------------------------

import math
import unittest

from aturtle import sprite

from . import fake_tkinter


class UnitSquare:

    def __init__(self):
        self.x_anchor = 0.5
        self.y_anchor = 0.5
        self.coords = [0, 0, 0, 1, 1, 1, 1, 0]


class TestSprite(unittest.TestCase):

    def setUp(self):

        self.canvas = fake_tkinter.FakeCanvas()


    def test_create(self):

        s = sprite.Sprite(self.canvas, UnitSquare())


    def test_default_x_anchor(self):

        s = sprite.Sprite(self.canvas, UnitSquare())
        self.assertEqual(s.x, 0)


    def test_default_y_anchor(self):

        s = sprite.Sprite(self.canvas, UnitSquare())
        self.assertEqual(s.y, 0)


    def test_coords_are_shape_coords_after_anchor_offset(self):

        shape = UnitSquare()
        s = sprite.Sprite(self.canvas, shape)

        shape_coords_after_offset = [c - 0.5 for c in shape.coords]
        self.assertEqual(s.coords, shape_coords_after_offset)


    def test_default_polygon_fill_color(self):

        s = sprite.Sprite(self.canvas, UnitSquare())

        create_polygon_kwargs = self.canvas._polygon_kwargs
        self.assertEqual(create_polygon_kwargs['fill'], '#009fff')


    def test_default_polygon_line_color(self):

        s = sprite.Sprite(self.canvas, UnitSquare())

        create_polygon_kwargs = self.canvas._polygon_kwargs
        self.assertEqual(create_polygon_kwargs['outline'], 'black')


    def test_default_polygon_line_width(self):

        s = sprite.Sprite(self.canvas, UnitSquare())

        create_polygon_kwargs = self.canvas._polygon_kwargs
        self.assertEqual(create_polygon_kwargs['width'], 2)


    def test_create_custom_anchor_x(self):

        s = sprite.Sprite(self.canvas, UnitSquare(), x=2, y=1)
        self.assertEqual(s.x, 2)


    def test_create_custom_anchor_y(self):

        s = sprite.Sprite(self.canvas, UnitSquare(), x=2, y=1)
        self.assertEqual(s.y, 1)


    def test_create_custom_anchor_coords(self):

        s = sprite.Sprite(self.canvas, UnitSquare(), x=2, y=1)

        shape_coords_after_offset = [1.5, 0.5, 1.5, 1.5, 2.5, 1.5, 2.5, 0.5]
        self.assertEqual(s.coords, shape_coords_after_offset)


    def test_create_custom_fill_color(self):

        s = sprite.Sprite(self.canvas, UnitSquare(), fill_color='pink')

        create_polygon_kwargs = self.canvas._polygon_kwargs
        self.assertEqual(create_polygon_kwargs['fill'], 'pink')


    def test_create_custom_line_color(self):

        s = sprite.Sprite(self.canvas, UnitSquare(), line_color='fuschia')

        create_polygon_kwargs = self.canvas._polygon_kwargs
        self.assertEqual(create_polygon_kwargs['outline'], 'fuschia')


    def test_create_custom_line_width(self):

        s = sprite.Sprite(self.canvas, UnitSquare(), line_width=1)

        create_polygon_kwargs = self.canvas._polygon_kwargs
        self.assertEqual(create_polygon_kwargs['width'], 1)


    def test_horizontal_move_moves_anchor_x(self):

        s = sprite.Sprite(self.canvas, UnitSquare())
        s.move(20, 0)
        self.assertEqual(s.x, 20)


    def test_vertical_move_moves_anchor_y(self):

        s = sprite.Sprite(self.canvas, UnitSquare())
        s.move(0, 10)
        self.assertEqual(s.y, 10)


    def test_move_does_not_call_canvas_update(self):

        s = sprite.Sprite(self.canvas, UnitSquare())
        s.move(0, 10)
        self.canvas.update.assert_not_called()


    def test_move_with_update_calls_calls_canvas_update(self):

        s = sprite.Sprite(self.canvas, UnitSquare())
        s.move(0, 10, update=True)
        self.canvas.update.assert_called_once_with()


    def test_horizontal_moveto_moves_anchor_x(self):

        s = sprite.Sprite(self.canvas, UnitSquare())
        s.moveto(20, 0)
        self.assertEqual(s.x, 20)


    def test_vertical_moveto_moves_anchor_y(self):

        s = sprite.Sprite(self.canvas, UnitSquare())
        s.moveto(0, 10)
        self.assertEqual(s.y, 10)


    def test_moveto_does_not_call_canvas_update(self):

        s = sprite.Sprite(self.canvas, UnitSquare())
        s.moveto(0, 10)
        self.canvas.update.assert_not_called()


    def test_moveto_with_update_calls_calls_canvas_update(self):

        s = sprite.Sprite(self.canvas, UnitSquare())
        s.moveto(0, 10, update=True)
        self.canvas.update.assert_called_once_with()


    def test_rotate_does_not_change_anchor_x(self):

        s = sprite.Sprite(self.canvas, UnitSquare())
        original_x = s.x

        s.rotate(1)
        self.assertEqual(original_x, s.x)


    def test_rotate_does_not_change_anchor_y(self):

        s = sprite.Sprite(self.canvas, UnitSquare())
        original_y = s.y

        s.rotate(1)
        self.assertEqual(original_y, s.y)


    def test_rotate_updates_coords(self):

        s = sprite.Sprite(self.canvas, UnitSquare())
        original_coords = list(s.coords)

        s.rotate(math.pi)
        # Half-circle rotated coords are easy to determine.
        expected_coords = original_coords[4:] + original_coords[:5]
        for orig, new in zip(expected_coords, s.coords):
            self.assertAlmostEqual(orig, new, places=5)


    def test_rotate_around_point_rotates_anchor_x(self):

        s = sprite.Sprite(self.canvas, UnitSquare())

        s.rotate(math.pi, around=(1, 1))
        self.assertAlmostEqual(s.x, 2, places=5)


    def test_rotate_around_point_rotates_anchor_y(self):

        s = sprite.Sprite(self.canvas, UnitSquare())

        s.rotate(math.pi, around=(1, 1))
        self.assertAlmostEqual(s.x, 2, places=5)


    def test_rotate_around_point_updates_coords(self):

        s = sprite.Sprite(self.canvas, UnitSquare())

        s.rotate(math.pi, around=(1, 1))
        # Half-circle rotated coords around (1, 1) are these.
        expected_coords = [2.5, 2.5, 2.5, 1.5, 1.5, 1.5, 1.5, 2.5]
        for orig, new in zip(expected_coords, s.coords):
            self.assertAlmostEqual(orig, new, places=5)


    def test_rotate_does_not_call_canvas_update(self):

        s = sprite.Sprite(self.canvas, UnitSquare())
        s.rotate(1)
        self.canvas.update.assert_not_called()


    def test_rotate_with_update_calls_calls_canvas_update(self):

        s = sprite.Sprite(self.canvas, UnitSquare())
        s.rotate(1, update=True)
        self.canvas.update.assert_called_once_with()


    def test_unrotate_does_not_change_anchor_x(self):

        s = sprite.Sprite(self.canvas, UnitSquare())
        original_x = s.x

        s.unrotate()
        self.assertEqual(original_x, s.x)


    def test_unrotate_does_not_change_anchor_y(self):

        s = sprite.Sprite(self.canvas, UnitSquare())
        original_y = s.y

        s.unrotate()
        self.assertEqual(original_y, s.y)


    def test_unrotate_does_not_call_canvas_update(self):

        s = sprite.Sprite(self.canvas, UnitSquare())
        s.unrotate()
        self.canvas.update.assert_not_called()


    def test_unrotate_with_update_calls_calls_canvas_update(self):

        s = sprite.Sprite(self.canvas, UnitSquare())
        s.unrotate(update=True)
        self.canvas.update.assert_called_once_with()


    def test_update_calls_canvas_update(self):

        s = sprite.Sprite(self.canvas, UnitSquare())

        s.update()
        self.canvas.update.assert_called_once_with()


    def test_delete_calls_canvas_delete(self):

        s = sprite.Sprite(self.canvas, UnitSquare())

        s.delete()
        self.canvas.delete.assert_called_once()


    def test_two_deletes_only_call_canvas_delete_once(self):

        s = sprite.Sprite(self.canvas, UnitSquare())

        s.delete()
        s.delete()
        self.canvas.delete.assert_called_once()
