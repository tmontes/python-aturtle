# ----------------------------------------------------------------------------
# Python A-Turtle
# ----------------------------------------------------------------------------
# Copyright (c) Tiago Montes.
# See LICENSE for details.
# ----------------------------------------------------------------------------

import itertools as it

from . import base


class Sprite(base.Sprite):

    def __init__(self, canvas, shape, *, anchor=(0, 0), angle=0, speed=360,
                 m_speed=None, r_speed=None, easing=None, m_easing=None,
                 r_easing=None, m_callback=None, r_callback=None, fps=80,
                 update=False):

        super().__init__(canvas, shape, anchor=anchor, angle=angle,
                         speed=speed, m_speed=m_speed, r_speed=r_speed,
                         easing=easing, m_easing=m_easing, r_easing=r_easing,
                         m_callback=m_callback, r_callback=r_callback,
                         fps=fps, update=update)

        self._id = self._canvas.create_polygon(
            self._offset_shape_coords(angle),
            fill=shape.fill_color,
            outline=shape.line_color,
            width=shape.line_width,
        )


    def _offset_shape_coords(self, angle):

        shape_coords = self._shape[angle]
        anchor_cycle = it.cycle(self._anchor)
        return [
            value + offset
            for value, offset in zip(shape_coords, anchor_cycle)
        ]


    @property
    def coords(self):

        return self._offset_shape_coords(self._angle)


    def direct_rotate(self, angle, *, around=None, update=None):

        # Rotate anchor point and update angle.
        super().direct_rotate(angle, around=around, update=False)

        # Use the shape for the new orientation.
        self._canvas.coords(self._id, self._offset_shape_coords(self._angle))

        self.update(update=update)
