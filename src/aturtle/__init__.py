# ----------------------------------------------------------------------------
# Python A-Turtle
# ----------------------------------------------------------------------------
# Copyright (c) Tiago Montes.
# See LICENSE for details.
# ----------------------------------------------------------------------------

"""
Python Async Turtle
"""


__version__ = '19.1.0a0'

__title__ = 'aturtle'
__description__ = 'Python A-Turtle'

__license__ = 'MIT'
__uri__ = 'https://github.com/tmontes/python-aturtle/'

__author__ = 'Tiago Montes'
__email__ = 'tiago.montes@gmail.com'


from . window import Window
from . shapes import Square, Bitmap
from . sprite import Sprite


__all__ = ['Window', 'Sprite', 'Square']


# ----------------------------------------------------------------------------
