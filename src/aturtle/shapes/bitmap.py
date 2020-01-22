# ----------------------------------------------------------------------------
# Python A-Turtle
# ----------------------------------------------------------------------------
# Copyright (c) Tiago Montes.
# See LICENSE for details.
# ----------------------------------------------------------------------------

"""
Bitmap Shapes.
"""

import base64
import io
import math

try:
    from PIL import Image, ImageTk
except ImportError:
    import tkinter
else:
    # Used at runtime to decide which code paths to take.
    tkinter = None

from . import base



class Shape(base.Shape):
    """
    A bitmap shape, created from either `filename` or `data`, with an `anchor`
    at the given (x, y) tuple.

    At least one of `filename` or `data` must be passed: the first is taken as
    the name of a bitmap image file on disk; the second is taken as a base-64
    encoded representation of such a file's in-memory payload.

    If the (x, y) anchor is int-based, the anchor is taken as an absolute
    position, starting from the bitmap's top left corner. When float-based,
    it is taken as a width/height relative position, with (0.0, 0.0) being the
    bitmap's top left corner and, for example, (0.5, 0.5) being the center of
    the bitmap.

    Creates rotated variations of the bitmap, accessible via indexing with an
    angle, where the source image is taken as angle 0. Rotated images are pre-
    computed by default, but can be created on demand if `pre_rotate` is false.

    The number of supported rotations is given by `rotations`, which must be
    a strictly positive integer.
    """


    def __init__(self, filename=None, data=None, *, anchor=(0.5, 0.5),
                 rotations=36, pre_rotate=True):

        if not filename and not data:
            raise ValueError('Need one of filename or data arguments.')

        if tkinter:
            kwargs = {'file': filename} if filename else {'data': data}
            image = tkinter.PhotoImage(**kwargs)
            width = image.width()
            height = image.height()
        else:
            # No tkinter, PIL was imported successfully.
            source = filename if filename else io.BytesIO(base64.b64decode(data))
            image = Image.open(source).convert('RGBA')
            width = image.width
            height = image.height

        ax, ay = anchor
        anchor = (
            int(ax * width) if isinstance(ax, float) else ax,
            int(ay * height) if isinstance(ay, float) else ay,
        )

        super().__init__(
            image=image,
            anchor=anchor,
            rotations=rotations,
            pre_rotate=pre_rotate,
        )


    def rotated_data(self, image, around, step, rotations):
        """
        Returns an `image` copy, rotated `step` * 360 degrees / `rotations`,
        around the `around` (x, y) tuple.
        """
        if tkinter:
            if step == 0:
                return image
            return self._rotated_tkinter(image, around, step, rotations)

        # No tkinter, PIL was imported successfully.
        if step == 0:
            return ImageTk.PhotoImage(image)
        return self._rotated_pil(image, around, step, rotations)


    def _rotated_tkinter(self, image, around, step, rotations):

        # tkinter-based image rotation

        w = image.width()
        h = image.height()

        ax, ay = around

        theta = math.pi * 2 * step / rotations

        pixel_rows = []
        transparency = {}

        for y in range(h):
            pixel_row = []
            for x in range(w):
                cos_theta = math.cos(theta)
                sin_theta = math.sin(theta)
                off_x = x - ax
                off_y = y - ay
                src_x = int(off_x * cos_theta - off_y * sin_theta) + ax
                src_y = int(off_x * sin_theta + off_y * cos_theta) + ay
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

        # PIL-based image rotation.

        theta = 360 * step / total

        rotated_pil_image = pil_image.rotate(
            theta,
            resample=Image.BICUBIC,
            center=around,
        )

        return ImageTk.PhotoImage(rotated_pil_image)
