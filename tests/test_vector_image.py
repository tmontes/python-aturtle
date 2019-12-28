# ----------------------------------------------------------------------------
# Python A-Turtle
# ----------------------------------------------------------------------------
# Copyright (c) Tiago Montes.
# See LICENSE for details.
# ----------------------------------------------------------------------------

import unittest

from aturtle.image import vector


class TestSquare(unittest.TestCase):

    def test_create(self):

        s = vector.Square()


    def _assert_equal_rounded_list_values(self, list_a, list_b):

        for a, b in zip(list_a, list_b):
            self.assertEqual(round(a), round(b))


    def test_default_coords(self):

        s = vector.Square()
        self._assert_equal_rounded_list_values(
            s.coords,
            [30, -30, 30, 30, -30, 30, -30, -30],
        )


    def test_default_anchor_x(self):

        s = vector.Square()
        self.assertEqual(s.x_anchor, 0)


    def test_default_anchor_y(self):

        s = vector.Square()
        self.assertEqual(s.y_anchor, 0)


    def test_custom_size_coords(self):

        s = vector.Square(side=42)
        self._assert_equal_rounded_list_values(
            s.coords,
            [21, -21, 21, 21, -21, 21, -21, -21]
        )


    def test_custom_size_anchor_x(self):

        s = vector.Square(side=42)
        self.assertEqual(s.x_anchor, 0)


    def test_custom_size_anchor_y(self):

        s = vector.Square(side=42)
        self.assertEqual(s.y_anchor, 0)
