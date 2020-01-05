# ----------------------------------------------------------------------------
# Python A-Turtle
# ----------------------------------------------------------------------------
# Copyright (c) Tiago Montes.
# See LICENSE for details.
# ----------------------------------------------------------------------------

import unittest


class TestCase(unittest.TestCase):

    def distance(self, x1, y1, x2, y2):

        dx_squared = (x1 - x2) ** 2
        dy_squared = (y1 - y2) ** 2
        return (dx_squared + dy_squared) ** 0.5


    def assert_almost_equal_anchor(self, left, right, places):

        lx, ly = left
        rx, ry = right
        self.assertAlmostEqual(lx, rx, places=places, msg='f{left=} != {right=}')
        self.assertAlmostEqual(ly, ry, places=places, msg='f{left=} != {right=}')


    def assert_almost_equal_coords(self, left, right, places):

        for offset, (l, r) in enumerate(zip(left, right)):
            msg = f'{left=} != {right=} at {offset=}'
            self.assertAlmostEqual(l, r, places=places, msg=msg)
