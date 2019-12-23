# ----------------------------------------------------------------------------
# Python A-Turtle
# ----------------------------------------------------------------------------
# Copyright (c) Tiago Montes.
# See LICENSE for details.
# ----------------------------------------------------------------------------

class Square:

    def __init__(self, side=32):

        half_side = side // 2

        self.x_center = half_side
        self.y_center = half_side


        self.coords = [
            0, 0,
            side, 0,
            side, side,
            0, side,
        ]
