# ----------------------------------------------------------------------------
# Python A-Turtle
# ----------------------------------------------------------------------------
# Copyright (c) Tiago Montes.
# See LICENSE for details.
# ----------------------------------------------------------------------------

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

        sprite_x, sprite_y = anchor
        shape_x, shape_y = shape.anchor
        self._id = self._canvas.create_image(
            sprite_x - shape_x,
            sprite_y - shape_y,
            image=shape[angle],
            anchor='sw',
        )


    def direct_rotate(self, angle, *, around=None, update=None):

        # Rotate anchor point and update angle.
        super().direct_rotate(angle, around=around, update=False)

        # Use the pre-rendered shape for the new orientation.
        self._canvas.itemconfig(self._id, image=self._shape[self._angle])

        self.update(update=update)
