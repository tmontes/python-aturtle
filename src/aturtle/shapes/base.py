# ----------------------------------------------------------------------------
# Python A-Turtle
# ----------------------------------------------------------------------------
# Copyright (c) Tiago Montes.
# See LICENSE for details.
# ----------------------------------------------------------------------------

"""
Shapes.
"""

import math


_CIRCLE_RADIANS = math.pi * 2



class Shape:
    """
    A shape, defined by `image`, with an `anchor` at the given (x, y) tuple.

    Creates rotated variations of the image, accessible via indexing with an
    angle, where the source image is taken as angle 0. Rotated image data is
    pre-computed if `pre_rotate` is true, and computed on access otherwise.
    In either case, the computed rotations are cached internally.

    The number of supported rotations is given by `rotations`, which must be
    a strictly positive integer.

    Image rotation code is provided by sub-classes implementing the
    `rotated_data` method.
    """

    def __init__(self, image, *, anchor, rotations, pre_rotate=True):

        self._image_source = image
        self._rotations = rotations
        self._pre_rotate = pre_rotate

        self._rotated_data = {}

        # Must compute at least this one to determine width and height,
        # in order to support floating point based anchors.
        unrotated = self.rotated_data(image, anchor, 0, rotations)
        self._rotated_data[0] = unrotated

        ax, ay = anchor
        self._anchor = (
            int(ax * unrotated.width()) if isinstance(ax, float) else ax,
            int(ay * unrotated.height()) if isinstance(ay, float) else ay,
        )

        if pre_rotate:
            for step in range(1, rotations):
                self._rotated_data[step] = self.rotated_data(
                    image=image,
                    around=self._anchor,
                    step=step,
                    rotations=rotations,
                )


    @property
    def anchor(self):
        """
        Image anchor as an (x, y) tuple.
        """
        return self._anchor


    def rotated_data(self, image, around, step, rotations):
        """
        Returns `image` rotated around the `around` (x, y) tuple.
        Rotation angle is `step` * 360 degrees / `rotations`.
        """
        raise NotImplementedError


    def __getitem__(self, radians):
        """
        Image data at the given angle.
        """
        rotations = self._rotations
        step = int(radians * rotations / _CIRCLE_RADIANS) % rotations

        rotated_data = self._rotated_data
        if not step in rotated_data and not self._pre_rotate:
            rotated_data[step] = self.rotated_data(
                image=self._image_source,
                around=self._anchor,
                step=step,
                rotations=rotations,
            )

        return rotated_data[step]
