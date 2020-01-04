# ----------------------------------------------------------------------------
# Python A-Turtle
# ----------------------------------------------------------------------------
# Copyright (c) Tiago Montes.
# See LICENSE for details.
# ----------------------------------------------------------------------------

from hypothesis import given
from hypothesis import strategies as st

from aturtle.shapes import vector

from . import base



class TestBadShapeCreation(base.TestCase):

    def test_create_with_bad_typed_coords_raises_TypeError(self):

        bad_values = (None, 42, 'hi', (i for i in range(10)))

        for bad_value in bad_values:
            with self.subTest(bad_value=bad_value):
                with self.assertRaises(TypeError):
                    _shape = vector.Shape(coords=bad_value)


    def test_create_with_odd_number_of_coords_raises_ValueError(self):

        with self.assertRaises(ValueError):
            _shape = vector.Shape([1, 2, 3])



class TestShapeAttributes(base.TestCase):

    def test_shape_anchor_is_tracked(self):

        anchor = (42, 24)
        shape = vector.Shape([0, 0, 2, 0, 1, 1], anchor=anchor)

        self.assertEqual(shape.anchor, anchor)



    def test_shape_fill_color_is_tracked(self):

        fill_color = 'nice hot pink'
        shape = vector.Shape([0, 0, 2, 0, 1, 1], fill_color=fill_color)

        self.assertEqual(shape.fill_color, fill_color)


    def test_shape_line_color_is_tracked(self):

        line_color = 'navy blue'
        shape = vector.Shape([0, 0, 2, 0, 1, 1], line_color=line_color)

        self.assertEqual(shape.line_color, line_color)


    def test_shape_line_width_is_tracked(self):

        line_width = 42
        shape = vector.Shape([0, 0, 2, 0, 1, 1], line_width=line_width)

        self.assertEqual(shape.line_width, line_width)



class TestShapeAccess(base.TestCase):

    def test_shape_at_angle_0_has_source_coords(self):

        coords = [0, 0, 2, 0, 1, 1]
        shape = vector.Shape(coords)

        result = shape[0]
        self.assert_almost_equal_coords(result, coords, places=1)


    def test_shape_coords_at_angle_90(self):

        shape = vector.Shape([0, 0, 2, 0, 1, 1])

        result = shape[90]
        self.assert_almost_equal_coords(result, [0, 0, 0, 2, -1, 1], places=1)


    def test_shape_coords_at_angle_180(self):

        shape = vector.Shape([0, 0, 2, 0, 1, 1])

        result = shape[180]
        self.assert_almost_equal_coords(result, [0, 0, -2, 0, -1, -1], places=1)


    def test_shape_coords_at_angle_270(self):

        shape = vector.Shape([0, 0, 2, 0, 1, 1])

        result = shape[270]
        self.assert_almost_equal_coords(result, [0, 0, 0, -2, 1, -1], places=1)



class TestBadRegularPolygonCreation(base.TestCase):

    def test_create_with_less_than_three_sides_raises_ValueError(self):

        for sides in range(-1, 3):
            with self.subTest(sides=sides):
                with self.assertRaises(ValueError):
                    _shape = vector.RegularPolygon(sides=sides, radius=42)


    def test_create_with_no_radius_or_side_raises_ValueError(self):

        with self.assertRaises(ValueError):
            _shape = vector.RegularPolygon(sides=5)


    def test_create_with_both_radius_and_side_raises_ValueError(self):

        with self.assertRaises(ValueError):
            _shape = vector.RegularPolygon(sides=5, radius=42, side=42)



class TestRegularPolygonAccess(base.TestCase):

    def test_4_sided_polygon_at_angle_0(self):

        shape = vector.RegularPolygon(sides=4, radius=10, angle=0)

        coords = shape[0]
        self.assert_almost_equal_coords(
            coords,
            [10, 0, 0, 10, -10, 0, 0, -10],
            places=1,
        )


    def test_4_sided_polygon_at_angle_45(self):

        shape = vector.RegularPolygon(sides=4, side=10, angle=45)

        coords = shape[0]
        self.assert_almost_equal_coords(
            coords,
            [5, -5, 5, 5, -5, 5, -5, -5],
            places=1,
        )


    @given(
        n_sides=st.integers(min_value=3, max_value=3600),
        radius=st.floats(min_value=0, exclude_min=True, max_value=1_000_000),
        ax=st.integers(min_value=1_000_000, max_value=1_000_000),
        ay=st.integers(min_value=1_000_000, max_value=1_000_000),
    )
    def test_N_sided_polygon_has_N_points(self, n_sides, radius, ax, ay):

        shape = vector.RegularPolygon(sides=n_sides, radius=radius, anchor=(ax, ay))
        # Two items (x, y) per point.
        n_points = len(shape[0]) // 2
        self.assertEqual(n_points, n_sides)


    @given(
        n_sides=st.integers(min_value=3, max_value=3600),
        radius=st.floats(min_value=0, exclude_min=True, max_value=1_000_000),
        ax=st.integers(min_value=1_000_000, max_value=1_000_000),
        ay=st.integers(min_value=1_000_000, max_value=1_000_000),
    )
    def test_all_points_equidistant_to_anchor(self, n_sides, radius, ax, ay):

        shape = vector.RegularPolygon(sides=n_sides, radius=radius, anchor=(ax, ay))
        coords = shape[0]
        for i in range(0, len(coords) // 2, 2):
            distance = self.distance(coords[i], coords[i+1], -ax, -ay)
            self.assertAlmostEqual(distance, radius, places=1)


    @given(
        n_sides=st.integers(min_value=3, max_value=3600),
        side=st.floats(min_value=0, exclude_min=True, max_value=1_000_000),
        ax=st.integers(min_value=1_000_000, max_value=1_000_000),
        ay=st.integers(min_value=1_000_000, max_value=1_000_000),
    )
    def test_all_points_at_side_distance_from_each_other(self, n_sides, side, ax, ay):

        shape = vector.RegularPolygon(sides=n_sides, side=side, anchor=(ax, ay))
        coords = shape[0]
        for i in range(0, len(coords) // 2, 2):
            distance = self.distance(*coords[i:i+4])
            self.assertAlmostEqual(distance, side, places=1)
        # Also assert distance from last to first.
        distance = self.distance(*coords[-2:], *coords[:2])
        self.assertAlmostEqual(distance, side, places=1)



class TestNamedRegularPolygons(base.TestCase):

    KNOWN_NAMED_POLYGONS = set((
        'Triangle',
        'Square',
        'Pentagon',
        'Hexagon',
        'Heptagon',
        'Octagon',
        'Nonagon',
        'Decagon',
        'Undecagon',
        'Dodecagon',
    ))

    def test_classes_are_discoverable(self):

        class_names = set(dir(vector))
        intersection = self.KNOWN_NAMED_POLYGONS.intersection(class_names)
        self.assertEqual(intersection, self.KNOWN_NAMED_POLYGONS)


    def test_classes_create_shapes(self):

        for class_name in self.KNOWN_NAMED_POLYGONS:
            with self.subTest(class_name=class_name):
                NamedPolygon = getattr(vector, class_name)
                _shape = NamedPolygon()



class TestBadStarCreation(base.TestCase):

    def test_less_than_2_points_raises_ValueError(self):

        with self.assertRaises(ValueError):
            _shape = vector.Star(points=1)



class TestStar(base.TestCase):

    def test_create(self):

        _shape = vector.Star()


    @given(
        points=st.integers(min_value=2, max_value=36),
    )
    def test_N_point_star_has_2N_points(self, points):

        shape = vector.Star(points=points)
        # Two items (x, y) per point.
        n_points = len(shape[0]) // 2
        self.assertEqual(n_points, points * 2)


    def test_integer_inner_radius_is_taken_as_is(self):

        shape = vector.Star(radius=42, inner_radius=24)
        coords = shape[0]

        # First point is radius away from origin.
        distance = self.distance(*coords[:2], 0, 0)
        self.assertAlmostEqual(distance, 42, places=1)

        # Last point is inner_radius away from origin
        distance = self.distance(*coords[-2:], 0, 0)
        self.assertAlmostEqual(distance, 24, places=1)


    def test_float_inner_radius_is_ratio_of_radius(self):

        shape = vector.Star(radius=1000, inner_radius=0.25)
        coords = shape[0]

        # First point is radius away from origin.
        distance = self.distance(*coords[:2], 0, 0)
        self.assertAlmostEqual(distance, 1000, places=1)

        # Last point is inner_radius away from origin
        distance = self.distance(*coords[-2:], 0, 0)
        self.assertAlmostEqual(distance, 250, places=1)


