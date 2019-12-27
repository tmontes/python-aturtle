# ----------------------------------------------------------------------------
# Python A-Turtle
# ----------------------------------------------------------------------------
# Copyright (c) Tiago Montes.
# See LICENSE for details.
# ----------------------------------------------------------------------------

import math

try:
    from PIL import Image, ImageTk
    tkinter = None
except ImportError:
    import tkinter


class Bitmap:

    def __init__(self, filename, *, cx=0.5, cy=0.5, rotations=36):

        if tkinter:
            pil_image = None
            image = tkinter.PhotoImage(file=filename)
        else:
            pil_image = Image.open(filename)
            image = ImageTk.PhotoImage(pil_image)

        w = image.width()
        h = image.height()

        cx = int(cx * w) if isinstance(cx, float) else cx
        cy = int(cy * h) if isinstance(cy, float) else cy

        images = {0: image}
        for step in range(1, rotations):
            if tkinter:
                rotated = self._rotated_tkinter(image, w, h, cx, cy, step, rotations)
            else:
                rotated = self._rotated_pil(pil_image, cx, cy, step, rotations)
            images[step] = rotated

        self._images = images
        self._cx = cx
        self._cy = cy
        self._rotations = rotations


    def _rotated_tkinter(self, image, w, h, cx, cy, step, total):

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


    def _rotated_pil(self, pil_image, cx, cy, step, total):

        neg_theta = -360 * step / total

        rotated_pil_image = pil_image.rotate(
            neg_theta,
            resample=Image.BICUBIC,
            center=(cx, cy),
        )

        return ImageTk.PhotoImage(rotated_pil_image)


    @property
    def cx(self):

        return self._cx


    @property
    def cy(self):

        return self._cy


    def __getitem__(self, theta):

        step = int(theta * self._rotations / (math.pi * 2)) % self._rotations
        return self._images[step]
