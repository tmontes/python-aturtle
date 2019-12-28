# ----------------------------------------------------------------------------
# Python A-Turtle
# ----------------------------------------------------------------------------
# Copyright (c) Tiago Montes.
# See LICENSE for details.
# ----------------------------------------------------------------------------

import math



class VectorShape:

    def __init__(self, points, *, anchor=(0, 0)):

        # TODO: Rename to self.points.
        self.coords = points
        self.x_anchor, self.y_anchor = anchor



class RegularPolygon(VectorShape):

    def __init__(self, *, sides, radius=None, side=None, angle=0, anchor=(0, 0)):

        if not radius and not side:
            raise ValueError('Need radius or side to be non-zero.')
        if radius and side:
            raise ValueError('Only one of radius or side can be set.')

        if side:
            radius = side / (2 * math.sin(math.pi / sides))

        points = []
        for step in range(sides):
            theta = math.pi * 2 * (step / sides) - angle
            x = radius * math.cos(theta)
            y = radius * math.sin(theta)
            # TODO: Should become a list of (x, y) tuples.
            points.extend((x, y))

        super().__init__(points, anchor=anchor)



_VECTOR_SHAPES = {}

def __getattr__(name):

    if name in _VECTOR_SHAPES:
        return _VECTOR_SHAPES[name]

    raise AttributeError(f'module {__name__!r} has no attribute {name!r}')



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
            def __init__(self, *, side=None, radius=42, angle=default_angle):
                radius = None if side else radius
                RegularPolygon.__init__(
                    self,
                    sides=number_of_sides,
                    side=side,
                    radius=radius,
                    angle=angle,
                )
            return __init__

        class_dict = dict(__init__=init_creator(sides, angle))
        Class = type(class_name, (RegularPolygon,), class_dict)
        _VECTOR_SHAPES[class_name] = Class


_create_regular_polygon_classes()
