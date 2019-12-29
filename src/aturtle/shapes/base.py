# ----------------------------------------------------------------------------
# Python A-Turtle
# ----------------------------------------------------------------------------
# Copyright (c) Tiago Montes.
# See LICENSE for details.
# ----------------------------------------------------------------------------

import math


_CIRCLE_RADIANS = math.pi * 2



class BaseShape:

    def __init__(self, image, *, anchor, rotations, pre_rotate=True):

        self._image_source = image
        self._rotations = rotations
        self._pre_rotate = pre_rotate

        self._rotated_sprite_data = {}

        # Must compute at least this one to determine width and height,
        # in order to support floating point based anchors.
        unrotated = self.rotated_sprite_data(image, anchor, 0, rotations)
        self._rotated_sprite_data[0] = unrotated

        ax, ay = anchor
        self._anchor = (
            int(ax * unrotated.width()) if isinstance(ax, float) else ax,
            int(ay * unrotated.height()) if isinstance(ay, float) else ay,
        )

        if pre_rotate:
            for step in range(1, rotations):
                self._rotated_sprite_data[step] = self.rotated_sprite_data(
                    image=image,
                    around=self._anchor,
                    step=step,
                    rotations=rotations,
                )


    def rotated_sprite_data(self, image, around, step, rotations):

        raise NotImplementedError


    def __getitem__(self, radians):

        rotations = self._rotations
        step = int(radians * rotations / _CIRCLE_RADIANS) % rotations

        rotated_sprite_data = self._rotated_sprite_data
        if not step in rotated_sprite_data and not self._pre_rotate:
            rotated_sprite_data[step] = self.rotated_sprite_data(
                image=self._image_source,
                around=self._anchor,
                step=step,
                rotations=rotations,
            )

        return rotated_sprite_data[step]
