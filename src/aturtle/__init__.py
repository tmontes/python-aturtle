# ----------------------------------------------------------------------------
# Python A-Turtle
# ----------------------------------------------------------------------------
# Copyright (c) Tiago Montes.
# See LICENSE for details.
# ----------------------------------------------------------------------------

"""
Python Async Turtle
"""


__version__ = '1.0.0a0'

__title__ = 'aturtle'
__description__ = 'Python A-Turtle'

__license__ = 'MIT'
__uri__ = 'https://github.com/tmontes/python-aturtle/'

__author__ = 'Tiago Montes'
__email__ = 'tiago.montes@gmail.com'


from . window import Window
from . import shapes
from . sprites import create_sprite
from . import turtle


__all__ = ['Window', 'create_sprite']


# ----------------------------------------------------------------------------
