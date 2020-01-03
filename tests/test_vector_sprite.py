# ----------------------------------------------------------------------------
# Python A-Turtle
# ----------------------------------------------------------------------------
# Copyright (c) Tiago Montes.
# See LICENSE for details.
# ----------------------------------------------------------------------------

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


    def test_default_anchor(self):

        s = sprites.VectorSprite(self.canvas, UnitSquare())
        self.assertEqual(s.anchor, (0, 0))


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


    def test_create_custom_anchor(self):

        s = sprites.VectorSprite(self.canvas, UnitSquare(), anchor=(2, 1))
        self.assertEqual(s.anchor, (2, 1))


    def test_create_custom_anchor_coords(self):

        s = sprites.VectorSprite(self.canvas, UnitSquare(), anchor=(2, 1))

        shape_coords_after_offset = [2.5, 0.5, 2.5, 1.5, 1.5, 1.5, 1.5, 0.5]
        self.assertEqual(s.coords, shape_coords_after_offset)


    def test_horizontal_move_moves_anchor(self):

        s = sprites.VectorSprite(self.canvas, UnitSquare())
        s.move(20, 0)
        self.assertEqual(s.anchor, (20, 0))


    def test_vertical_move_moves_anchor(self):

        s = sprites.VectorSprite(self.canvas, UnitSquare())
        s.move(0, 10)
        self.assertEqual(s.anchor, (0, 10))


    def test_move_does_not_call_canvas_update_idletasks(self):

        s = sprites.VectorSprite(self.canvas, UnitSquare())
        s.move(0, 10)
        self.canvas.update_idletasks.assert_not_called()


    def test_move_with_update_calls_canvas_update_idletasks(self):

        s = sprites.VectorSprite(self.canvas, UnitSquare())
        s.move(0, 10, update=True)
        self.canvas.update_idletasks.assert_called_once_with()


    def test_horizontal_move_to_moves_anchor(self):

        s = sprites.VectorSprite(self.canvas, UnitSquare())
        s.move_to(20, 0)
        self.assertEqual(s.anchor, (20, 0))


    def test_vertical_move_to_moves_anchor(self):

        s = sprites.VectorSprite(self.canvas, UnitSquare())
        s.move_to(0, 10)
        self.assertEqual(s.anchor, (0, 10))


    def test_move_to_does_not_call_canvas_update_idletasks(self):

        s = sprites.VectorSprite(self.canvas, UnitSquare())
        s.move_to(0, 10)
        self.canvas.update_idletasks.assert_not_called()


    def test_move_to_with_update_calls_canvas_update_idletasks(self):

        s = sprites.VectorSprite(self.canvas, UnitSquare())
        s.move_to(0, 10, update=True)
        self.canvas.update_idletasks.assert_called_once_with()


    def test_rotate_does_not_change_anchor(self):

        s = sprites.VectorSprite(self.canvas, UnitSquare())
        original_anchor = s.anchor

        s.rotate(1)
        self.assertEqual(original_anchor, s.anchor)


    def test_rotate_updates_coords(self):

        s = sprites.VectorSprite(self.canvas, UnitSquare())
        original_coords = list(s.coords)

        s.rotate(180)
        # Half-circle rotated coords are easy to determine.
        expected_coords = original_coords[4:] + original_coords[:5]
        for orig, new in zip(expected_coords, s.coords):
            self.assertAlmostEqual(orig, new, places=5)


    def test_rotate_around_point_rotates_anchor(self):

        s = sprites.VectorSprite(self.canvas, UnitSquare())

        s.rotate(180, around=(1, 1))
        self.assertEqual(s.anchor, (2, 2))


    def test_rotate_around_point_updates_coords(self):

        s = sprites.VectorSprite(self.canvas, UnitSquare())

        s.rotate(180, around=(1, 1))
        # Half-circle rotated coords around (1, 1) are these.
        expected_coords = [1.5, 2.5, 1.5, 1.5, 2.5, 1.5, 2.5, 2.5]
        for orig, new in zip(expected_coords, s.coords):
            self.assertAlmostEqual(orig, new, places=5)


    def test_rotate_does_not_call_canvas_update_idletasks(self):

        s = sprites.VectorSprite(self.canvas, UnitSquare())
        s.rotate(1)
        self.canvas.update_idletasks.assert_not_called()


    def test_rotate_with_update_calls_canvas_update_idletasks(self):

        s = sprites.VectorSprite(self.canvas, UnitSquare())
        s.rotate(1, update=True)
        self.canvas.update_idletasks.assert_called_once_with()


    def test_rotate_to_does_not_change_anchor(self):

        s = sprites.VectorSprite(self.canvas, UnitSquare())
        original_anchor = s.anchor

        s.rotate_to()
        self.assertEqual(original_anchor, s.anchor)


    def test_rotate_to_does_not_call_canvas_update_idletasks(self):

        s = sprites.VectorSprite(self.canvas, UnitSquare())
        s.rotate_to()
        self.canvas.update_idletasks.assert_not_called()


    def test_rotate_to_with_update_calls_canvas_update_idletasks(self):

        s = sprites.VectorSprite(self.canvas, UnitSquare())
        s.rotate_to(update=True)
        self.canvas.update_idletasks.assert_called_once_with()


    def test_update_calls_canvas_update_idletasks(self):

        s = sprites.VectorSprite(self.canvas, UnitSquare())

        s.update()
        self.canvas.update_idletasks.assert_called_once_with()


    def test_delete_calls_canvas_delete(self):

        s = sprites.VectorSprite(self.canvas, UnitSquare())

        s.delete()
        self.canvas.delete.assert_called_once()


    def test_two_deletes_only_call_canvas_delete_once(self):

        s = sprites.VectorSprite(self.canvas, UnitSquare())

        s.delete()
        s.delete()
        self.canvas.delete.assert_called_once()
