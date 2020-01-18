# ----------------------------------------------------------------------------
# Python A-Turtle
# ----------------------------------------------------------------------------
# Copyright (c) Tiago Montes.
# See LICENSE for details.
# ----------------------------------------------------------------------------

from aturtle import turtle

from . import base
from . import fake_tkinter
from . import fake_sprite



class TestTurtle(base.TestCase):

    def setUp(self):

        self.canvas = fake_tkinter.FakeCanvas()
        self.sprite = fake_sprite.FakeSprite(
            canvas=self.canvas,
            anchor=(0, 0),
            angle=0,
        )


    def test_create_turtle_default_down(self):

        t = turtle.Turtle(self.sprite)
        self.assertIs(t.down, True)


    def test_create_turtle_default_line_color(self):

        t = turtle.Turtle(self.sprite)
        self.assertEqual(t.line_color, '#cccccc')


    def test_create_turtle_default_line_width(self):

        t = turtle.Turtle(self.sprite)
        self.assertEqual(t.line_width, 3)


    def test_create_turtle_anchor_from_sprite(self):

        t = turtle.Turtle(self.sprite)
        self.assertEqual(t.anchor, (0, 0))


    def test_create_turtle_angle_from_sprite(self):

        t = turtle.Turtle(self.sprite)
        self.assertEqual(t.angle, 0)


    def test_create_turtle_explicit_down_True(self):

        t = turtle.Turtle(self.sprite, down=True)
        self.assertIs(t.down, True)


    def test_create_turtle_explicit_down_False(self):

        t = turtle.Turtle(self.sprite, down=False)
        self.assertIs(t.down, False)


    def test_create_turtle_explicit_line_color(self):

        t = turtle.Turtle(self.sprite, line_color='orange')
        self.assertEqual(t.line_color, 'orange')


    def test_create_turtle_explicit_line_width(self):

        t = turtle.Turtle(self.sprite, line_width=42)
        self.assertEqual(t.line_width, 42)


