# ----------------------------------------------------------------------------
# Python A-Turtle
# ----------------------------------------------------------------------------
# Copyright (c) Tiago Montes.
# See LICENSE for details.
# ----------------------------------------------------------------------------

import math
import tkinter


class Bitmap:

    def __init__(self, source, cx=0.5, cy=0.5, *, rotations=36):

        image = tkinter.PhotoImage(file=source)

        w = image.width()
        h = image.height()

        cx = int(cx * w) if isinstance(cx, float) else cx
        cy = int(cy * h) if isinstance(cy, float) else cy

        images = {0: image}
        for step in range(1, rotations):
            images[step] = self._rotated(image, w, h, cx, cy, step, rotations)

        self._images = images
        self._rotations = rotations
        self._cx = cx
        self._cy = cy


    def _rotated(self, image, w, h, cx, cy, step, total):

        neg_theta = -math.pi * 2 * step / total

        pixel_rows = []
        transparency = {}

        for y in range(image.height()):
            pixel_row = []
            for x in range(image.width()):
                cos_neg_theta = math.cos(neg_theta)
                sin_neg_theta = math.sin(neg_theta)
                off_x = x - cx
                off_y = y - cy
                src_x = int(off_x * cos_neg_theta - off_y * sin_neg_theta) + cx
                src_y = int(off_x * sin_neg_theta + off_y * cos_neg_theta) + cy
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


    @property
    def cx(self):

        return self._cx


    @property
    def cy(self):

        return self._cy


    def __getitem__(self, theta):

        step = int(theta * self._rotations / (math.pi * 2)) % self._rotations
        return self._images[step]
