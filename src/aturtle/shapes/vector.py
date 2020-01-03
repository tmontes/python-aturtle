# ----------------------------------------------------------------------------
# Python A-Turtle
# ----------------------------------------------------------------------------
# Copyright (c) Tiago Montes.
# See LICENSE for details.
# ----------------------------------------------------------------------------

"""
Vector Shapes.
"""

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
    """
    A vector shape, created from `coords`, with an `anchor` at the given (x, y)
    tuple. Visual attributes are set with `fill_color`, `line_color`, and
    `line_width`.

    The `coords` argument should be a list/tuple with an even count of numbers,
    consisting of alternating x and y canvas coordinates that define a sequence
    polygon points.

    Creates rotated variations of the polygon, accessible via indexing with
    an angle, where the source polygon is taken as angle 0. Rotated data is
    computed on demand, but can be pre-computed if `pre_rotate` is true.

    The number of supported rotations is given by `rotations`, which must be
    a strictly positive integer.
    """

    def __init__(self, coords, *, anchor=(0, 0), fill_color=_FILL_COLOR,
                 line_color=_LINE_COLOR, line_width=_LINE_WIDTH, rotations=360,
                 pre_rotate=False):

        if not isinstance(coords, (list, tuple)):
            raise TypeError('coords must be a list or a tuple')

        if len(coords) % 2:
            raise ValueError('coords must have an even number of coordinates')

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
        """
        The polygon's fill color.
        """
        return self._fill_color


    @property
    def line_color(self):
        """
        The polygon's line color.
        """
        return self._line_color


    @property
    def line_width(self):
        """
        The polygon's line width.
        """
        return self._line_width


    def rotated_data(self, image, around, step, rotations):
        """
        Returns a list with the coordinates in the `image` list rotated
        `step` * 360 degrees / `rotations`, around the `around` (x, y) tuple.
        """
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
    """
    A regular polygon vector shape with as many sides as specified in `sides`,
    and either the specified `radius` or with sides with length `side`. The
    `angle` argument, in degrees, rotates the polygon points by that amount.

    See the `Shape` base class docs for info on the other __init__ arguments.
    """

    def __init__(self, *, sides, radius=None, side=None, angle=0, anchor=(0, 0),
                 fill_color=_FILL_COLOR, line_color=_LINE_COLOR,
                 line_width=_LINE_WIDTH, rotations=360, pre_rotate=False):

        if sides < 3:
            raise ValueError('Must have more than two sides.')

        if not radius and not side:
            raise ValueError('Need radius or side to be non-zero.')
        if radius and side:
            raise ValueError('Only one of radius or side can be set.')

        if side:
            radius = side / (2 * math.sin(math.pi / sides))

        coords = []
        for step in range(sides):
            theta = (360 * step / sides) - angle
            theta_rad = theta * math.pi / 180
            x = radius * math.cos(theta_rad)
            y = radius * math.sin(theta_rad)
            coords.extend((x, y))

        super().__init__(
            coords,
            anchor=anchor,
            fill_color=fill_color,
            line_color=line_color,
            line_width=line_width,
            rotations=rotations,
            pre_rotate=pre_rotate,
        )



def _create_regular_polygon_classes():

    # Called at import time (see below), dynamically creates classes for all
    # the regular poligons with 3-12 sides.

    regular_polygons = [
        dict(name='Triangle', sides=3, angle=90),
        dict(name='Square', sides=4, angle=45),
        dict(name='Pentagon', sides=5, angle=90),
        dict(name='Hexagon', sides=6, angle=90),
        dict(name='Heptagon', sides=7, angle=90),
        dict(name='Octagon', sides=8, angle=22.5),
        dict(name='Nonagon', sides=9, angle=90),
        dict(name='Decagon', sides=10, angle=90),
        dict(name='Undecagon', sides=11, angle=90),
        dict(name='Dodecagon', sides=12, angle=90),
    ]

    for polygon_spec in regular_polygons:

        class_name = polygon_spec['name']
        sides = polygon_spec['sides']
        angle = polygon_spec['angle']

        def init_creator(number_of_sides, default_angle):
            def __init__(self, *, side=None, radius=42, angle=default_angle,
                         anchor=(0, 0), fill_color=_FILL_COLOR,
                         line_color=_LINE_COLOR, line_width=_LINE_WIDTH,
                         rotations=360, pre_rotate=False):
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
                    rotations=rotations,
                    pre_rotate=pre_rotate,
                )
            return __init__

        class_dict = dict(__init__=init_creator(sides, angle))
        Class = type(class_name, (RegularPolygon,), class_dict)
        Class.__doc__ = f"""
            A {class_name} vector shape.

            See the `RegularPolygon` class docs for info the __init__ arguments.
        """
        _VECTOR_SHAPE_CLASSES[class_name] = Class
        export_class(Class)

_create_regular_polygon_classes()



@export_class
class Star(Shape):
    """
    A star vector shape with points, radius, and inner-radius given by the
    equally named arguments. The `angle` argument, in radians, rotates the star
    points by that amount.

    See the `Shape` base class docs for info on the other __init__ arguments.
    """

    def __init__(self, *, points=5, radius=42, inner_radius=0.5, angle=0,
                 anchor=(0, 0), fill_color=_FILL_COLOR, line_color=_LINE_COLOR,
                 line_width=_LINE_WIDTH, rotations=360, pre_rotate=False):

        if points < 2:
            raise ValueError('Must have at least two points.')

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
            rotations=rotations,
            pre_rotate=pre_rotate,
        )
