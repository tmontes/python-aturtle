# ----------------------------------------------------------------------------
# Python A-Turtle
# ----------------------------------------------------------------------------
# Copyright (c) Tiago Montes.
# See LICENSE for details.
# ----------------------------------------------------------------------------

import unittest

from aturtle.sprites import base

from . import fake_tkinter



class TestDefaultSprite(unittest.TestCase):

    def setUp(self):

        self.canvas = fake_tkinter.FakeCanvas()


    def test_create(self):

        _sprite = base.Sprite(canvas=self.canvas, shape=None)


    def test_default_anchor(self):

        sprite = base.Sprite(canvas=self.canvas, shape=None)
        self.assertEqual(sprite.anchor, (0, 0))


    def test_default_angle(self):

        sprite = base.Sprite(canvas=self.canvas, shape=None)
        self.assertEqual(sprite.angle, 0)


    def test_move_moves_anchor(self):

        sprite = base.Sprite(canvas=self.canvas, shape=None)
        sprite.move(42, 24)
        self.assertEqual(sprite.anchor, (42, 24))


    def test_move_moves_anchor_relative(self):

        sprite = base.Sprite(canvas=self.canvas, shape=None)
        sprite.move(42, 0)
        sprite.move(0, 24)
        self.assertEqual(sprite.anchor, (42, 24))


    def test_move_does_not_change_angle(self):

        sprite = base.Sprite(canvas=self.canvas, shape=None)
        sprite.move(42, 24)
        self.assertEqual(sprite.angle, 0)


    def test_move_to_moves_anchor(self):

        sprite = base.Sprite(canvas=self.canvas, shape=None)
        sprite.move_to(42, 24)
        self.assertEqual(sprite.anchor, (42, 24))


    def test_move_to_moves_anchor_absolute(self):

        sprite = base.Sprite(canvas=self.canvas, shape=None)
        sprite.move_to(42, 0)
        sprite.move_to(0, 24)
        self.assertEqual(sprite.anchor, (0, 24))


    def test_move_to_does_not_change_angle(self):

        sprite = base.Sprite(canvas=self.canvas, shape=None)
        sprite.move_to(42, 24)
        self.assertEqual(sprite.angle, 0)


    def test_rotate_does_not_move_anchor(self):

        sprite = base.Sprite(canvas=self.canvas, shape=None)
        sprite.rotate(90)
        self.assertEqual(sprite.anchor, (0, 0))


    def test_rotate_around_moves_anchor(self):

        sprite = base.Sprite(canvas=self.canvas, shape=None)
        sprite.rotate(180, around=(1, 1))
        ax, ay = sprite.anchor
        self.assertAlmostEqual(ax, 2, places=1)
        self.assertAlmostEqual(ay, 2, places=1)


    def test_rotate_around_moves_anchor_relative(self):

        sprite = base.Sprite(canvas=self.canvas, shape=None)
        sprite.rotate(90, around=(1, 1))
        sprite.rotate(90, around=(1, 1))
        ax, ay = sprite.anchor
        self.assertAlmostEqual(ax, 2, places=1)
        self.assertAlmostEqual(ay, 2, places=1)


    def test_rotate_changes_angle(self):

        sprite = base.Sprite(canvas=self.canvas, shape=None)
        sprite.rotate(90)
        self.assertEqual(sprite.angle, 90)


    def test_rotate_changes_angle_relative(self):

        sprite = base.Sprite(canvas=self.canvas, shape=None)
        sprite.rotate(45)
        sprite.rotate(45)
        self.assertEqual(sprite.angle, 90)


    def test_rotate_around_changes_angle(self):

        sprite = base.Sprite(canvas=self.canvas, shape=None)
        sprite.rotate(90, around=(1, 1))
        self.assertEqual(sprite.angle, 90)


    def test_rotate_to_does_not_move_anchor(self):

        sprite = base.Sprite(canvas=self.canvas, shape=None)
        sprite.rotate_to(90)
        self.assertEqual(sprite.anchor, (0, 0))


    def test_rotate_to_around_moves_anchor(self):

        sprite = base.Sprite(canvas=self.canvas, shape=None)
        sprite.rotate_to(180, around=(1, 1))
        self.assertEqual(sprite.anchor, (2, 2))


    def test_rotate_to_around_moves_anchor_absolute(self):

        sprite = base.Sprite(canvas=self.canvas, shape=None)
        sprite.rotate_to(90, around=(1, 1))
        sprite.rotate_to(180, around=(1, 1))
        self.assertEqual(sprite.anchor, (2, 2))


    def test_rotate_to_changes_angle(self):

        sprite = base.Sprite(canvas=self.canvas, shape=None)
        sprite.rotate_to(90)
        self.assertEqual(sprite.angle, 90)


    def test_rotate_to_changes_angle_absolute(self):

        sprite = base.Sprite(canvas=self.canvas, shape=None)
        sprite.rotate_to(20)
        sprite.rotate_to(90)
        self.assertEqual(sprite.angle, 90)


    def test_rotate_to_around_changes_angle(self):

        sprite = base.Sprite(canvas=self.canvas, shape=None)
        sprite.rotate_to(90, around=(1, 1))
        self.assertEqual(sprite.angle, 90)


    def test_update_calls_canvas_update_idletasks(self):

        sprite = base.Sprite(canvas=self.canvas, shape=None)
        sprite.update()
        self.canvas.update_idletasks.assert_called_once_with()


    def test_move_with_no_update_calls_canvas_update_idletasks(self):

        sprite = base.Sprite(canvas=self.canvas, shape=None)
        sprite.move(42, 24)
        self.canvas.update_idletasks.assert_not_called()


    def test_move_with_update_calls_canvas_update_idletasks(self):

        sprite = base.Sprite(canvas=self.canvas, shape=None)
        sprite.move(42, 24, update=True)
        self.canvas.update_idletasks.assert_called_once_with()


    def test_move_to_with_no_update_calls_canvas_update_idletasks(self):

        sprite = base.Sprite(canvas=self.canvas, shape=None)
        sprite.move_to(42, 24)
        self.canvas.update_idletasks.assert_not_called()


    def test_move_to_with_update_calls_canvas_update_idletasks(self):

        sprite = base.Sprite(canvas=self.canvas, shape=None)
        sprite.move_to(42, 24, update=True)
        self.canvas.update_idletasks.assert_called_once_with()


    def test_rotate_with_no_update_calls_canvas_update_idletasks(self):

        sprite = base.Sprite(canvas=self.canvas, shape=None)
        sprite.rotate(42)
        self.canvas.update_idletasks.assert_not_called()


    def test_rotate_with_update_calls_canvas_update_idletasks(self):

        sprite = base.Sprite(canvas=self.canvas, shape=None)
        sprite.rotate(42, update=True)
        self.canvas.update_idletasks.assert_called_once_with()


    def test_rotate_to_with_no_update_calls_canvas_update_idletasks(self):

        sprite = base.Sprite(canvas=self.canvas, shape=None)
        sprite.rotate_to(42)
        self.canvas.update_idletasks.assert_not_called()


    def test_rotate_to_with_update_calls_canvas_update_idletasks(self):

        sprite = base.Sprite(canvas=self.canvas, shape=None)
        sprite.rotate_to(42, update=True)
        self.canvas.update_idletasks.assert_called_once_with()



class TestNonDefaultSprite(unittest.TestCase):

    def setUp(self):

        self.canvas = fake_tkinter.FakeCanvas()
        self.sprite = base.Sprite(
            canvas=self.canvas,
            shape=None,
            anchor=(42, 24),
            angle=42,
        )


    def test_anchor(self):

        self.assertEqual(self.sprite.anchor, (42, 24))


    def test_angle(self):

        self.assertEqual(self.sprite.angle, 42)


    def test_move_with_no_args_does_not_move_anchor(self):

        self.sprite.move()
        self.assertEqual(self.sprite.anchor, (42, 24))


    def test_move_moves_anchor(self):

        self.sprite.move(-42, -24)
        self.assertEqual(self.sprite.anchor, (0, 0))


    def test_move_moves_anchor_relative(self):

        self.sprite.move(-42, 0)
        self.sprite.move(0, -24)
        self.assertEqual(self.sprite.anchor, (0, 0))


    def test_move_does_not_change_angle(self):

        self.sprite.move(42, 24)
        self.assertEqual(self.sprite.angle, 42)


    def test_move_to_moves_anchor(self):

        self.sprite.move_to(20, 10)
        self.assertEqual(self.sprite.anchor, (20, 10))


    def test_move_to_moves_anchor_absolute(self):

        self.sprite.move_to(42, 0)
        self.sprite.move_to(0, 24)
        self.assertEqual(self.sprite.anchor, (0, 24))


    def test_move_to_does_not_change_angle(self):

        self.sprite.move_to(42, 24)
        self.assertEqual(self.sprite.angle, 42)


    def test_rotate_does_not_move_anchor(self):

        self.sprite.rotate(90)
        self.assertEqual(self.sprite.anchor, (42, 24))


    def test_rotate_around_moves_anchor(self):

        self.sprite.rotate(180, around=(0, 0))
        ax, ay = self.sprite.anchor
        self.assertAlmostEqual(ax, -42, places=1)
        self.assertAlmostEqual(ay, -24, places=1)


    def test_rotate_around_moves_anchor_relative(self):

        self.sprite.rotate(90, around=(0, 0))
        self.sprite.rotate(90, around=(0, 0))
        ax, ay = self.sprite.anchor
        self.assertAlmostEqual(ax, -42, places=1)
        self.assertAlmostEqual(ay, -24, places=1)


    def test_rotate_changes_angle(self):

        self.sprite.rotate(-42)
        self.assertAlmostEqual(self.sprite.angle, 0, places=1)


    def test_rotate_changes_angle_relative(self):

        self.sprite.rotate(-40)
        self.sprite.rotate(-2)
        self.assertAlmostEqual(self.sprite.angle, 0, places=1)


    def test_rotate_around_changes_angle(self):

        self.sprite.rotate(-42, around=(1, 1))
        self.assertAlmostEqual(self.sprite.angle, 0)


    def test_rotate_to_does_not_move_anchor(self):

        self.sprite.rotate_to(90)
        self.assertEqual(self.sprite.anchor, (42, 24))


    def test_rotate_to_around_moves_anchor(self):

        self.sprite.rotate_to(42+180, around=(0, 0))
        ax, ay = self.sprite.anchor
        self.assertAlmostEqual(ax, -42, places=1)
        self.assertAlmostEqual(ay, -24, places=1)


    def test_rotate_to_around_moves_anchor_absolute(self):

        self.sprite.rotate_to(90, around=(0, 0))
        self.sprite.rotate_to(42+180, around=(0, 0))
        ax, ay = self.sprite.anchor
        self.assertAlmostEqual(ax, -42, places=1)
        self.assertAlmostEqual(ay, -24, places=1)


    def test_rotate_to_changes_angle(self):

        self.sprite.rotate_to(90)
        self.assertEqual(self.sprite.angle, 90)


    def test_rotate_to_changes_angle_absolute(self):

        self.sprite.rotate_to(20)
        self.sprite.rotate_to(90)
        self.assertEqual(self.sprite.angle, 90)


    def test_rotate_to_around_changes_angle(self):

        self.sprite.rotate_to(90, around=(1, 1))
        self.assertEqual(self.sprite.angle, 90)


    def test_update_calls_canvas_update_idletasks(self):

        self.sprite.update()
        self.canvas.update_idletasks.assert_called_once_with()


    def test_move_with_no_update_calls_canvas_update_idletasks(self):

        self.sprite.move(42, 24)
        self.canvas.update_idletasks.assert_not_called()


    def test_move_with_update_calls_canvas_update_idletasks(self):

        self.sprite.move(42, 24, update=True)
        self.canvas.update_idletasks.assert_called_once_with()


    def test_move_to_with_no_update_calls_canvas_update_idletasks(self):

        self.sprite.move_to(42, 24)
        self.canvas.update_idletasks.assert_not_called()


    def test_move_to_with_update_calls_canvas_update_idletasks(self):

        self.sprite.move_to(42, 24, update=True)
        self.canvas.update_idletasks.assert_called_once_with()


    def test_rotate_with_no_update_calls_canvas_update_idletasks(self):

        self.sprite.rotate(42)
        self.canvas.update_idletasks.assert_not_called()


    def test_rotate_with_update_calls_canvas_update_idletasks(self):

        self.sprite.rotate(42, update=True)
        self.canvas.update_idletasks.assert_called_once_with()


    def test_rotate_to_with_no_update_calls_canvas_update_idletasks(self):

        self.sprite.rotate_to(42)
        self.canvas.update_idletasks.assert_not_called()


    def test_rotate_to_with_update_calls_canvas_update_idletasks(self):

        self.sprite.rotate_to(42, update=True)
        self.canvas.update_idletasks.assert_called_once_with()

