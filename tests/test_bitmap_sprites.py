# ----------------------------------------------------------------------------
# Python A-Turtle
# ----------------------------------------------------------------------------
# Copyright (c) Tiago Montes.
# See LICENSE for details.
# ----------------------------------------------------------------------------

from aturtle import sprites

from . import sprite_test_helpers
from . import fake_tkinter



class FakeBitmapShape:

    def __init__(self, anchor=(42, 24)):
        self.anchor = anchor

    def __getitem__(self, angle):
        return f'image-at-angle-{angle}'



class TestDefaultSprite(sprite_test_helpers.TestCase):

    def setUp(self):

        self.canvas = fake_tkinter.FakeCanvas()


    def test_create(self):

        _sprite = sprites.BitmapSprite(self.canvas, FakeBitmapShape())


    def test_default_anchor(self):

        sprite = sprites.BitmapSprite(self.canvas, FakeBitmapShape())
        self.assert_almost_equal_anchor(sprite.anchor, (0, 0), places=1)


    def test_default_angle(self):

        sprite = sprites.BitmapSprite(self.canvas, FakeBitmapShape())
        self.assertAlmostEqual(sprite.angle, 0, places=1)


    def test_create_calls_canvas_create_image(self):

        shape = FakeBitmapShape(anchor=(10, 10))
        _sprite = sprites.BitmapSprite(self.canvas, shape)

        create_image = self.canvas.create_image
        create_image.assert_called_once_with(
            -10,
            -10,
            image='image-at-angle-0',
            anchor='nw',
        )


    def test_rotate_calls_canvas_itemconfig_with_rotated_shape(self):

        sprite = sprites.BitmapSprite(self.canvas, FakeBitmapShape())
        sprite.rotate(180)

        canvas_itemconfig = self.canvas.itemconfig
        canvas_itemconfig.assert_called_once_with(
            24,
            image='image-at-angle-180',
        )


    def test_rotate_around_point_rotates_anchor(self):

        sprite = sprites.BitmapSprite(self.canvas, FakeBitmapShape())

        sprite.rotate(180, around=(1, 1))
        self.assert_almost_equal_anchor(sprite.anchor, (2, 2), places=1)


    def test_rotate_around_point_calls_canvas_itemconfig(self):

        sprite = sprites.BitmapSprite(self.canvas, FakeBitmapShape())

        sprite.rotate(180, around=(1, 1))

        canvas_itemconfig = self.canvas.itemconfig
        canvas_itemconfig.assert_called_once_with(
            24,
            image='image-at-angle-180',
        )


    def test_rotate_around_point_calls_canvas_moveto(self):

        shape = FakeBitmapShape(anchor=(0, 0))
        sprite = sprites.BitmapSprite(self.canvas, shape)

        sprite.rotate(180, around=(1, 1))

        canvas_moveto = self.canvas.moveto
        canvas_moveto.assert_called_once_with(24, 2, 2)


    def test_rotate_does_not_call_canvas_update_idletasks(self):

        sprite = sprites.BitmapSprite(self.canvas, FakeBitmapShape())
        sprite.rotate(1)
        self.canvas.update_idletasks.assert_not_called()


    def test_rotate_with_update_calls_canvas_update_idletasks(self):

        sprite = sprites.BitmapSprite(self.canvas, FakeBitmapShape())
        sprite.rotate(1, update=True)
        self.canvas.update_idletasks.assert_called_once_with()
