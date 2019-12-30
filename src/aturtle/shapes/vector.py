# ----------------------------------------------------------------------------
# Python A-Turtle
# ----------------------------------------------------------------------------
# Copyright (c) Tiago Montes.
# See LICENSE for details.
# ----------------------------------------------------------------------------

import math

from . import base



# Populated by the `export_class` decorator.

__all__ = []

def export_class(cls):

    __all__.append(cls.__name__)
    return cls



# Track dynamically created classes.

_VECTOR_SHAPE_CLASSES = {}


def __getattr__(name):

    # Give access dynamically created classes (see PEP-562).

    if name in _VECTOR_SHAPE_CLASSES:
        return _VECTOR_SHAPE_CLASSES[name]

    raise AttributeError(f'module {__name__!r} has no attribute {name!r}')



def __dir__():

    # Expose exported classes (see PEP-562).

    return __all__



_FILL_COLOR = '#009fff'
_LINE_COLOR = 'black'
_LINE_WIDTH = 2



@export_class
class Shape(base.Shape):

    def __init__(self, coords, *, anchor=(0, 0), fill_color=_FILL_COLOR,
                 line_color=_LINE_COLOR, line_width=_LINE_WIDTH, rotations=360,
                 pre_rotate=False):

        super().__init__(
            coords,
            anchor=anchor,
            rotations=rotations,
            pre_rotate=pre_rotate,
        )

        self._fill_color = fill_color
        self._line_color = line_color
        self._line_width = line_width


    @property
    def fill_color(self):

        return self._fill_color


    @property
    def line_color(self):

        return self._line_color


    @property
    def line_width(self):

        return self._line_width


    def rotated_data(self, image, around, step, rotations):

        theta = math.pi * 2 * step / rotations
        sin_theta = math.sin(theta)
        cos_theta = math.cos(theta)
        ax, ay = around

        coords = list(self._image_source)
        for i in range(0, len(coords)-1, 2):
            x = coords[i] - ax
            y = coords[i+1] - ay
            coords[i] = x * cos_theta - y * sin_theta
            coords[i+1] = x * sin_theta + y * cos_theta

        return coords



@export_class
class RegularPolygon(Shape):

    def __init__(self, *, sides, radius=None, side=None, angle=0, anchor=(0, 0),
                 fill_color=_FILL_COLOR, line_color=_LINE_COLOR,
                 line_width=_LINE_WIDTH):

        if not radius and not side:
            raise ValueError('Need radius or side to be non-zero.')
        if radius and side:
            raise ValueError('Only one of radius or side can be set.')

        if side:
            radius = side / (2 * math.sin(math.pi / sides))

        coords = []
        for step in range(sides):
            theta = math.pi * 2 * (step / sides) - angle
            x = radius * math.cos(theta)
            y = radius * math.sin(theta)
            coords.extend((x, y))

        super().__init__(
            coords,
            anchor=anchor,
            fill_color=fill_color,
            line_color=line_color,
            line_width=line_width,
        )



def _create_regular_polygon_classes():

    half_pi = math.pi / 2
    quarter_pi = math.pi / 4
    eight_pi = math.pi / 8

    regular_polygons = [
        dict(name='Triangle', sides=3, angle=half_pi),
        dict(name='Square', sides=4, angle=quarter_pi),
        dict(name='Pentagon', sides=5, angle=half_pi),
        dict(name='Hexagon', sides=6, angle=half_pi),
        dict(name='Heptagon', sides=7, angle=half_pi),
        dict(name='Octagon', sides=8, angle=eight_pi),
        dict(name='Nonagon', sides=9, angle=half_pi),
        dict(name='Decagon', sides=10, angle=half_pi),
        dict(name='Undecagon', sides=11, angle=half_pi),
        dict(name='Dodecagon', sides=12, angle=half_pi),
    ]

    for polygon_spec in regular_polygons:

        class_name = polygon_spec['name']
        sides = polygon_spec['sides']
        angle = polygon_spec['angle']

        def init_creator(number_of_sides, default_angle):
            def __init__(self, *, side=None, radius=42, angle=default_angle,
                         anchor=(0, 0), fill_color=_FILL_COLOR,
                         line_color=_LINE_COLOR, line_width=_LINE_WIDTH):
                radius = None if side else radius
                RegularPolygon.__init__(
                    self,
                    sides=number_of_sides,
                    side=side,
                    radius=radius,
                    angle=angle,
                    anchor=anchor,
                    fill_color=fill_color,
                    line_color=line_color,
                    line_width=line_width,
                )
            return __init__

        class_dict = dict(__init__=init_creator(sides, angle))
        Class = type(class_name, (RegularPolygon,), class_dict)
        _VECTOR_SHAPE_CLASSES[class_name] = Class
        export_class(Class)

_create_regular_polygon_classes()



@export_class
class Star(Shape):

    def __init__(self, *, points=5, radius=42, inner_radius=0.5, angle=0,
                 anchor=(0, 0), fill_color=_FILL_COLOR, line_color=_LINE_COLOR,
                 line_width=_LINE_WIDTH):

        if isinstance(inner_radius, float):
            inner_radius = inner_radius * radius

        steps = points * 2

        coords = []
        for step in range(steps):
            theta = math.pi * 2 * (step / steps) + angle
            point_radius = inner_radius if step % 2 else radius
            x = point_radius * math.sin(theta)
            y = -point_radius * math.cos(theta)
            coords.extend((x, y))

        super().__init__(
            coords,
            anchor=anchor,
            fill_color=fill_color,
            line_color=line_color,
            line_width=line_width,
        )
