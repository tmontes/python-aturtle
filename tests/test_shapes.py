# ----------------------------------------------------------------------------
# Python A-Turtle
# ----------------------------------------------------------------------------
# Copyright (c) Tiago Montes.
# See LICENSE for details.
# ----------------------------------------------------------------------------

import unittest

from aturtle import shapes


class TestSquare(unittest.TestCase):

    def test_create(self):

        s = shapes.Square()


    def test_default_coords(self):

        s = shapes.Square()
        self.assertEqual(
            s.coords,
            [0, 0, 32, 0, 32, 32, 0, 32],
        )


    def test_default_anchor_x(self):

        s = shapes.Square()
        self.assertEqual(s.x_anchor, 16)


    def test_default_anchor_y(self):

        s = shapes.Square()
        self.assertEqual(s.y_anchor, 16)


    def test_custom_size_coords(self):

        s = shapes.Square(side=42)
        self.assertEqual(
            s.coords,
            [0, 0, 42, 0, 42, 42, 0, 42],
        )


    def test_custom_size_anchor_x(self):

        s = shapes.Square(side=42)
        self.assertEqual(s.x_anchor, 21)


    def test_custom_size_anchor_y(self):

        s = shapes.Square(side=42)
        self.assertEqual(s.y_anchor, 21)
