# ----------------------------------------------------------------------------
# Python A-Turtle
# ----------------------------------------------------------------------------
# Copyright (c) Tiago Montes.
# See LICENSE for details.
# ----------------------------------------------------------------------------

import math


_CIRCLE_RADIANS = math.pi * 2



class BaseShape:

    def __init__(self, data, *, anchor, rotations, pre_rotate=True):

        self._source_data = data
        self._anchor = anchor
        self._rotations = rotations
        self._pre_rotate = pre_rotate

        self._rotated_sprite_data = {}
        if pre_rotate:
            for step in range(rotations):
                self._rotated_sprite_data[step] = self.rotated_sprite_data(
                    data=data,
                    around=anchor,
                    step=step,
                    rotations=rotations,
                )


    def sprite_data(self, data):

        return f'sprite-data({data!r})'


    def rotated_sprite_data(self, data, around, step, rotations):

        print(f'{self=} {data=} {around=} {step=} {rotations=}')
        if not step:
            return self.sprite_data(data)
        return self.sprite_data(f'{data}-{step}/{rotations}-around-{around}')


    def __getitem__(self, radians):

        rotations = self._rotations
        step = int(radians * rotations / _CIRCLE_RADIANS) % rotations

        rotated_sprite_data = self._rotated_sprite_data
        if not step in rotated_sprite_data and not self._pre_rotate:
            rotated_sprite_data[step] = self.rotated_sprite_data(
                data=self._source_data,
                around=self._anchor,
                step=step,
                rotations=rotations,
            )

        return rotated_sprite_data[step]
