# ----------------------------------------------------------------------------
# Python A-Turtle
# ----------------------------------------------------------------------------
# Copyright (c) Tiago Montes.
# See LICENSE for details.
# ----------------------------------------------------------------------------

import base64
import io
import math

try:
    from PIL import Image, ImageTk
    tkinter = None
except ImportError:
    import tkinter

from . import base



class Bitmap(base.BaseShape):

    def __init__(self, filename=None, data=None, *, anchor=(0.5, 0.5),
                 rotations=36, pre_rotate=True):

        if not filename and not data:
            raise ValueError('Need one of filename or data arguments.')

        if tkinter:
            kwargs = {'file': filename} if filename else {'data': data}
            image = tkinter.PhotoImage(**kwargs)
        else:
            source = filename if filename else io.BytesIO(base64.b64decode(data))
            image = Image.open(source)

        super().__init__(
            image=image,
            anchor=anchor,
            rotations=rotations,
            pre_rotate=pre_rotate,
        )


    def rotated_sprite_data(self, image, around, step, rotations):

        if tkinter:
            if step == 0:
                return image
            return self._rotated_tkinter(image, around, step, rotations)

        if step == 0:
            return ImageTk.PhotoImage(image)
        return self._rotated_pil(image, around, step, rotations)


    def _rotated_tkinter(self, image, around, step, rotations):

        w = image.width()
        h = image.height()

        ax, ay = around

        neg_theta = -math.pi * 2 * step / rotations

        pixel_rows = []
        transparency = {}

        for y in range(h):
            pixel_row = []
            for x in range(w):
                cos_neg_theta = math.cos(neg_theta)
                sin_neg_theta = math.sin(neg_theta)
                off_x = x - ax
                off_y = y - ay
                src_x = int(off_x * cos_neg_theta - off_y * sin_neg_theta) + ax
                src_y = int(off_x * sin_neg_theta + off_y * cos_neg_theta) + ay
                if (0 <= src_x < w) and (0 <= src_y < h):
                    red, green, blue = image.get(src_x, src_y)
                    transp = image.transparency_get(src_x, src_y)
                else:
                    red, green, blue = 255, 255, 255
                    transp = True
                pixel_row.append(f'#{red:02x}{green:02x}{blue:02x}')
                transparency[(x, y)] = transp
            pixel_rows.append(pixel_row)

        rotated = image.copy()
        rotated.put(pixel_rows)
        for (x, y), transp in transparency.items():
            rotated.transparency_set(x, y, transp)

        return rotated


    def _rotated_pil(self, pil_image, around, step, total):

        neg_theta = -360 * step / total

        rotated_pil_image = pil_image.rotate(
            neg_theta,
            resample=Image.BICUBIC,
            center=around,
        )

        return ImageTk.PhotoImage(rotated_pil_image)


    @property
    def cx(self):

        return self._anchor[0]


    @property
    def cy(self):

        return self._anchor[1]
