# ----------------------------------------------------------------------------
# Python A-Turtle
# ----------------------------------------------------------------------------
# Copyright (c) Tiago Montes.
# See LICENSE for details.
# ----------------------------------------------------------------------------

from aturtle import sprites, shapes

from . import base
from . import fake_tkinter



class UnitSquare(shapes.vector.Square):

    def __init__(self, fill_color=None, line_color=None, line_width=None):

        super().__init__(
            side=1,
            fill_color=fill_color,
            line_color=line_color,
            line_width=line_width,
        )



class TestDefaultSprite(base.TestCase):

    def setUp(self):

        self.canvas = fake_tkinter.FakeCanvas()


    def test_create(self):

        _sprite = sprites.VectorSprite(self.canvas, UnitSquare())


    def test_default_anchor(self):

        sprite = sprites.VectorSprite(self.canvas, UnitSquare())
        self.assert_almost_equal_anchor(sprite.anchor, (0, 0), places=1)


    def test_default_angle(self):

        sprite = sprites.VectorSprite(self.canvas, UnitSquare())
        self.assertAlmostEqual(sprite.angle, 0, places=1)


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
        self.assert_almost_equal_coords(sprite.coords, expected_coords, places=1)


    def test_direct_move_moves_coords(self):

        sprite = sprites.VectorSprite(self.canvas, UnitSquare())
        sprite.direct_move(2, 1)

        expected_coords = [2.5, 0.5, 2.5, 1.5, 1.5, 1.5, 1.5, 0.5]
        self.assert_almost_equal_coords(
            sprite.coords,
            expected_coords,
            places=1,
        )


    def test_direct_move_to_moves_coords(self):

        sprite = sprites.VectorSprite(self.canvas, UnitSquare())
        sprite.direct_move_to(2, 1)
        expected_coords = [2.5, 0.5, 2.5, 1.5, 1.5, 1.5, 1.5, 0.5]
        self.assert_almost_equal_coords(
            sprite.coords,
            expected_coords,
            places=1,
        )


    def test_direct_rotate_updates_coords(self):

        sprite = sprites.VectorSprite(self.canvas, UnitSquare())
        original_coords = list(sprite.coords)

        sprite.direct_rotate(180)
        # Half-circle rotated coords are easy to determine.
        expected_coords = original_coords[4:] + original_coords[:5]
        self.assert_almost_equal_coords(
            sprite.coords,
            expected_coords,
            places=1,
        )


    def test_direct_rotate_around_point_rotates_anchor(self):

        sprite = sprites.VectorSprite(self.canvas, UnitSquare())

        sprite.direct_rotate(180, around=(1, 1))
        self.assert_almost_equal_anchor(sprite.anchor, (2, 2), places=1)


    def test_direct_rotate_around_point_updates_coords(self):

        sprite = sprites.VectorSprite(self.canvas, UnitSquare())

        sprite.direct_rotate(180, around=(1, 1))
        # Half-circle rotated coords around (1, 1) are these.
        expected_coords = [1.5, 2.5, 1.5, 1.5, 2.5, 1.5, 2.5, 2.5]
        for orig, new in zip(expected_coords, sprite.coords):
            self.assertAlmostEqual(orig, new, places=5)


    def test_direct_rotate_to_does_not_change_anchor(self):

        sprite = sprites.VectorSprite(self.canvas, UnitSquare())
        original_anchor = sprite.anchor

        sprite.direct_rotate_to()
        self.assert_almost_equal_anchor(original_anchor, sprite.anchor, places=1)


    def test_direct_move_does_not_call_canvas_update(self):

        sprite = sprites.VectorSprite(self.canvas, UnitSquare())
        sprite.direct_move(0, 10)
        self.canvas.update.assert_not_called()


    def test_direct_move_with_update_calls_canvas_update(self):

        sprite = sprites.VectorSprite(self.canvas, UnitSquare())
        sprite.direct_move(0, 10, update=True)
        self.canvas.update.assert_called_once_with()


    def test_direct_move_to_does_not_call_canvas_update(self):

        sprite = sprites.VectorSprite(self.canvas, UnitSquare())
        sprite.direct_move_to(0, 10)
        self.canvas.update.assert_not_called()


    def test_direct_move_to_with_update_calls_canvas_update(self):

        sprite = sprites.VectorSprite(self.canvas, UnitSquare())
        sprite.direct_move_to(0, 10, update=True)
        self.canvas.update.assert_called_once_with()


    def test_direct_rotate_does_not_call_canvas_update(self):

        sprite = sprites.VectorSprite(self.canvas, UnitSquare())
        sprite.direct_rotate(1)
        self.canvas.update.assert_not_called()


    def test_direct_rotate_with_update_calls_canvas_update(self):

        sprite = sprites.VectorSprite(self.canvas, UnitSquare())
        sprite.direct_rotate(1, update=True)
        self.canvas.update.assert_called_once_with()


    def test_direct_rotate_to_does_not_call_canvas_update(self):

        sprite = sprites.VectorSprite(self.canvas, UnitSquare())
        sprite.direct_rotate_to()
        self.canvas.update.assert_not_called()


    def test_direct_rotate_to_with_update_calls_canvas_update(self):

        sprite = sprites.VectorSprite(self.canvas, UnitSquare())
        sprite.direct_rotate_to(update=True)
        self.canvas.update.assert_called_once_with()


    def test_delete_calls_canvas_delete(self):

        sprite = sprites.VectorSprite(self.canvas, UnitSquare())

        sprite.delete()
        self.canvas.delete.assert_called_once()


    def test_two_deletes_only_call_canvas_delete_once(self):

        sprite = sprites.VectorSprite(self.canvas, UnitSquare())

        sprite.delete()
        sprite.delete()
        self.canvas.delete.assert_called_once()



class TestNonDefaultSprite(base.TestCase):

    def setUp(self):

        self.canvas = fake_tkinter.FakeCanvas()


    def test_custom_anchor(self):

        sprite = sprites.VectorSprite(self.canvas, UnitSquare(), anchor=(2, 1))
        self.assert_almost_equal_anchor(sprite.anchor, (2, 1), places=1)


    def test_custom_angle(self):

        sprite = sprites.VectorSprite(self.canvas, UnitSquare(), angle=42)
        self.assertAlmostEqual(sprite.angle, 42, places=1)


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


    def test_direct_move_moves_coords(self):

        sprite = sprites.VectorSprite(self.canvas, UnitSquare(), anchor=(1, 0))
        sprite.direct_move(1, 1)

        expected_coords = [2.5, 0.5, 2.5, 1.5, 1.5, 1.5, 1.5, 0.5]
        self.assert_almost_equal_coords(
            sprite.coords,
            expected_coords,
            places=1,
        )


    def test_direct_move_to_moves_coords(self):

        sprite = sprites.VectorSprite(self.canvas, UnitSquare(), anchor=(5, 5))
        sprite.direct_move_to(2, 1)
        expected_coords = [2.5, 0.5, 2.5, 1.5, 1.5, 1.5, 1.5, 0.5]
        self.assert_almost_equal_coords(
            sprite.coords,
            expected_coords,
            places=1,
        )


    def test_direct_rotate_updates_coords(self):

        sprite = sprites.VectorSprite(self.canvas, UnitSquare(), angle=180)
        original_coords = list(sprite.coords)

        sprite.direct_rotate(180)
        # Half-circle rotated coords are easy to determine.
        expected_coords = original_coords[4:] + original_coords[:5]
        self.assert_almost_equal_coords(
            sprite.coords,
            expected_coords,
            places=1,
        )


    def test_direct_rotate_around_point_rotates_anchor(self):

        sprite = sprites.VectorSprite(self.canvas, UnitSquare(), anchor=(2, 1))

        sprite.direct_rotate(180, around=(0, 0))
        self.assert_almost_equal_anchor(sprite.anchor, (-2, -1), places=1)


    def test_direct_rotate_around_point_updates_coords(self):

        sprite = sprites.VectorSprite(self.canvas, UnitSquare(), anchor=(1, 1))

        sprite.direct_rotate(180, around=(0, 0))
        expected_coords = [-1.5, -0.5, -1.5, -1.5, -0.5, -1.5, -0.5, -0.5]
        self.assert_almost_equal_coords(
            sprite.coords,
            expected_coords,
            places=1,
        )


    def test_direct_rotate_to_does_not_change_anchor(self):

        sprite = sprites.VectorSprite(self.canvas, UnitSquare(), angle=42)
        original_anchor = sprite.anchor

        sprite.direct_rotate_to()
        self.assert_almost_equal_anchor(original_anchor, sprite.anchor, places=1)

