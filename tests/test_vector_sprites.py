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



class _TestBase(unittest.TestCase):

    def assert_almost_equal_coords(self, left, right, places):

        for offset, (l, r) in enumerate(zip(left, right)):
            msg = f'{left=} != {right=} at {offset=}'
            self.assertAlmostEqual(l, r, places=places, msg=msg)


    def assert_anchor_almost_equal(self, a1, a2, places):

        a1_x, a1_y = a1
        a2_x, a2_y = a2
        self.assertAlmostEqual(a1_x, a2_x, places=places)
        self.assertAlmostEqual(a1_y, a2_y, places=places)



class TestDefaultSprite(_TestBase):

    def setUp(self):

        self.canvas = fake_tkinter.FakeCanvas()


    def test_create(self):

        _sprite = sprites.VectorSprite(self.canvas, UnitSquare())


    def test_default_anchor(self):

        sprite = sprites.VectorSprite(self.canvas, UnitSquare())
        self.assertEqual(sprite.anchor, (0, 0))


    def test_default_angle(self):

        sprite = sprites.VectorSprite(self.canvas, UnitSquare())
        self.assertEqual(sprite.angle, 0)


    def test_shape_fill_color_passed_to_create_polygon_fill_kwarg(self):

        _sprite = sprites.VectorSprite(self.canvas, UnitSquare(fill_color='#009fff'))

        create_polygon_kwargs = self.canvas.create_polygon_kwargs
        self.assertEqual(create_polygon_kwargs['fill'], '#009fff')


    def test_shape_line_color_passed_to_create_polygon_outline_kwarg(self):

        _sprite = sprites.VectorSprite(self.canvas, UnitSquare(line_color='black'))

        create_polygon_kwargs = self.canvas.create_polygon_kwargs
        self.assertEqual(create_polygon_kwargs['outline'], 'black')


    def test_shape_line_width_passed_to_create_polygon_width_kwarg(self):

        _sprite = sprites.VectorSprite(self.canvas, UnitSquare(line_width=2))

        create_polygon_kwargs = self.canvas.create_polygon_kwargs
        self.assertEqual(create_polygon_kwargs['width'], 2)


    def test_shape_coords(self):

        square = UnitSquare()
        sprite = sprites.VectorSprite(self.canvas, square)
        expected_coords = square[0]
        self.assertEqual(sprite.coords, expected_coords)


    def test_move_moves_coords(self):

        sprite = sprites.VectorSprite(self.canvas, UnitSquare())
        sprite.move(2, 1)

        expected_coords = [2.5, 0.5, 2.5, 1.5, 1.5, 1.5, 1.5, 0.5]
        self.assert_almost_equal_coords(
            sprite.coords,
            expected_coords,
            places=1,
        )


    def test_move_to_moves_coords(self):

        sprite = sprites.VectorSprite(self.canvas, UnitSquare())
        sprite.move_to(2, 1)
        expected_coords = [2.5, 0.5, 2.5, 1.5, 1.5, 1.5, 1.5, 0.5]
        self.assert_almost_equal_coords(
            sprite.coords,
            expected_coords,
            places=1,
        )


    def test_rotate_updates_coords(self):

        sprite = sprites.VectorSprite(self.canvas, UnitSquare())
        original_coords = list(sprite.coords)

        sprite.rotate(180)
        # Half-circle rotated coords are easy to determine.
        expected_coords = original_coords[4:] + original_coords[:5]
        self.assert_almost_equal_coords(
            sprite.coords,
            expected_coords,
            places=1,
        )


    def test_rotate_around_point_rotates_anchor(self):

        sprite = sprites.VectorSprite(self.canvas, UnitSquare())

        sprite.rotate(180, around=(1, 1))
        self.assertEqual(sprite.anchor, (2, 2))


    def test_rotate_around_point_updates_coords(self):

        sprite = sprites.VectorSprite(self.canvas, UnitSquare())

        sprite.rotate(180, around=(1, 1))
        # Half-circle rotated coords around (1, 1) are these.
        expected_coords = [1.5, 2.5, 1.5, 1.5, 2.5, 1.5, 2.5, 2.5]
        for orig, new in zip(expected_coords, sprite.coords):
            self.assertAlmostEqual(orig, new, places=5)


    def test_rotate_to_does_not_change_anchor(self):

        sprite = sprites.VectorSprite(self.canvas, UnitSquare())
        original_anchor = sprite.anchor

        sprite.rotate_to()
        self.assertEqual(original_anchor, sprite.anchor)


    def test_move_does_not_call_canvas_update_idletasks(self):

        sprite = sprites.VectorSprite(self.canvas, UnitSquare())
        sprite.move(0, 10)
        self.canvas.update_idletasks.assert_not_called()


    def test_move_with_update_calls_canvas_update_idletasks(self):

        sprite = sprites.VectorSprite(self.canvas, UnitSquare())
        sprite.move(0, 10, update=True)
        self.canvas.update_idletasks.assert_called_once_with()


    def test_move_to_does_not_call_canvas_update_idletasks(self):

        sprite = sprites.VectorSprite(self.canvas, UnitSquare())
        sprite.move_to(0, 10)
        self.canvas.update_idletasks.assert_not_called()


    def test_move_to_with_update_calls_canvas_update_idletasks(self):

        sprite = sprites.VectorSprite(self.canvas, UnitSquare())
        sprite.move_to(0, 10, update=True)
        self.canvas.update_idletasks.assert_called_once_with()


    def test_rotate_does_not_call_canvas_update_idletasks(self):

        sprite = sprites.VectorSprite(self.canvas, UnitSquare())
        sprite.rotate(1)
        self.canvas.update_idletasks.assert_not_called()


    def test_rotate_with_update_calls_canvas_update_idletasks(self):

        sprite = sprites.VectorSprite(self.canvas, UnitSquare())
        sprite.rotate(1, update=True)
        self.canvas.update_idletasks.assert_called_once_with()


    def test_rotate_to_does_not_call_canvas_update_idletasks(self):

        sprite = sprites.VectorSprite(self.canvas, UnitSquare())
        sprite.rotate_to()
        self.canvas.update_idletasks.assert_not_called()


    def test_rotate_to_with_update_calls_canvas_update_idletasks(self):

        sprite = sprites.VectorSprite(self.canvas, UnitSquare())
        sprite.rotate_to(update=True)
        self.canvas.update_idletasks.assert_called_once_with()


    def test_update_calls_canvas_update_idletasks(self):

        sprite = sprites.VectorSprite(self.canvas, UnitSquare())

        sprite.update()
        self.canvas.update_idletasks.assert_called_once_with()


    def test_delete_calls_canvas_delete(self):

        sprite = sprites.VectorSprite(self.canvas, UnitSquare())

        sprite.delete()
        self.canvas.delete.assert_called_once()


    def test_two_deletes_only_call_canvas_delete_once(self):

        sprite = sprites.VectorSprite(self.canvas, UnitSquare())

        sprite.delete()
        sprite.delete()
        self.canvas.delete.assert_called_once()



class TestNonDefaultSprite(_TestBase):

    def setUp(self):

        self.canvas = fake_tkinter.FakeCanvas()


    def test_custom_anchor(self):

        sprite = sprites.VectorSprite(self.canvas, UnitSquare(), anchor=(2, 1))
        self.assertEqual(sprite.anchor, (2, 1))


    def test_custom_angle(self):

        sprite = sprites.VectorSprite(self.canvas, UnitSquare(), angle=42)
        self.assertEqual(sprite.angle, 42)


    def test_custom_anchor_coords(self):

        sprite = sprites.VectorSprite(self.canvas, UnitSquare(), anchor=(2, 1))

        expected_coords = [2.5, 0.5, 2.5, 1.5, 1.5, 1.5, 1.5, 0.5]
        self.assert_almost_equal_coords(
            sprite.coords,
            expected_coords,
            places=1,
        )


    def test_custom_angle_coords(self):

        sprite = sprites.VectorSprite(self.canvas, UnitSquare(), angle=180)

        expected_coords = [-0.5, 0.5, -0.5, -0.5, 0.5, -0.5, 0.5, 0.5]
        self.assert_almost_equal_coords(
            sprite.coords,
            expected_coords,
            places=1,
        )


    def test_move_moves_coords(self):

        sprite = sprites.VectorSprite(self.canvas, UnitSquare(), anchor=(1, 0))
        sprite.move(1, 1)

        expected_coords = [2.5, 0.5, 2.5, 1.5, 1.5, 1.5, 1.5, 0.5]
        self.assert_almost_equal_coords(
            sprite.coords,
            expected_coords,
            places=1,
        )


    def test_move_to_moves_coords(self):

        sprite = sprites.VectorSprite(self.canvas, UnitSquare(), anchor=(5, 5))
        sprite.move_to(2, 1)
        expected_coords = [2.5, 0.5, 2.5, 1.5, 1.5, 1.5, 1.5, 0.5]
        self.assert_almost_equal_coords(
            sprite.coords,
            expected_coords,
            places=1,
        )


    def test_rotate_updates_coords(self):

        sprite = sprites.VectorSprite(self.canvas, UnitSquare(), angle=180)
        original_coords = list(sprite.coords)

        sprite.rotate(180)
        # Half-circle rotated coords are easy to determine.
        expected_coords = original_coords[4:] + original_coords[:5]
        self.assert_almost_equal_coords(
            sprite.coords,
            expected_coords,
            places=1,
        )


    def test_rotate_around_point_rotates_anchor(self):

        sprite = sprites.VectorSprite(self.canvas, UnitSquare(), anchor=(2, 1))

        sprite.rotate(180, around=(0, 0))
        self.assert_anchor_almost_equal(sprite.anchor, (-2, -1), places=1)


    def test_rotate_around_point_updates_coords(self):

        sprite = sprites.VectorSprite(self.canvas, UnitSquare(), anchor=(1, 1))

        sprite.rotate(180, around=(0, 0))
        expected_coords = [-1.5, -0.5, -1.5, -1.5, -0.5, -1.5, -0.5, -0.5]
        self.assert_almost_equal_coords(
            sprite.coords,
            expected_coords,
            places=1,
        )


    def test_rotate_to_does_not_change_anchor(self):

        sprite = sprites.VectorSprite(self.canvas, UnitSquare(), angle=42)
        original_anchor = sprite.anchor

        sprite.rotate_to()
        self.assertEqual(original_anchor, sprite.anchor)

