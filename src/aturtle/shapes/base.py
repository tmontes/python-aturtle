# ----------------------------------------------------------------------------
# Python A-Turtle
# ----------------------------------------------------------------------------
# Copyright (c) Tiago Montes.
# See LICENSE for details.
# ----------------------------------------------------------------------------

import functools
import math


_CIRCLE_RADIANS = math.pi * 2



class BaseShape:

    def __init__(self, data, *, anchor, rotations, pre_rotate=True):

        self._source_data = data
        self._anchor = anchor
        self._rotations = rotations
        self._pre_rotate = pre_rotate

        if pre_rotate:
            for step in range(rotations):
                # Pass args by name, as in __getitem__, or pre-cache won't work.
                _ = self.rotated_sprite_data(
                    data=data,
                    around=anchor,
                    step=step,
                    rotations=rotations,
                )


    def sprite_data(self, data):

        return f'sprite-data({data!r})'


    @functools.lru_cache(maxsize=360)
    def rotated_sprite_data(self, data, around, step, rotations):

        print(f'{self=} {data=} {around=} {step=} {rotations=}')
        if not step:
            return self.sprite_data(data)
        return self.sprite_data(f'{data}-{step}/{rotations}-around-{around}')


    def __getitem__(self, radians):

        rotations = self._rotations

        # Pass args by name, as in __init__, or pre-cache won't work.
        return self.rotated_sprite_data(
            data=self._source_data,
            around=self._anchor,
            step=int(radians * rotations / _CIRCLE_RADIANS) % rotations,
            rotations=rotations,
        )
