# ----------------------------------------------------------------------------
# Python A-Turtle
# ----------------------------------------------------------------------------
# Copyright (c) Tiago Montes.
# See LICENSE for details.
# ----------------------------------------------------------------------------

"""
Shapes.
"""



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

        if not isinstance(anchor, (tuple, list)):
            raise TypeError('anchor must be a tuple or a list')

        if rotations < 1:
            raise ValueError('rotations must be strictly positive')

        self._image_source = image
        self._anchor = anchor
        self._rotations = rotations
        self._pre_rotate = pre_rotate

        self._rotated_data = {}
        if pre_rotate:
            for step in range(rotations):
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


    def __getitem__(self, angle):
        """
        Image data at the given angle, in degrees.
        """
        rotations = self._rotations
        step = round(angle * rotations / 360) % rotations

        rotated_data = self._rotated_data
        if not step in rotated_data and not self._pre_rotate:
            rotated_data[step] = self.rotated_data(
                image=self._image_source,
                around=self._anchor,
                step=step,
                rotations=rotations,
            )

        return rotated_data[step]
