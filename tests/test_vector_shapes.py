# ----------------------------------------------------------------------------
# Python A-Turtle
# ----------------------------------------------------------------------------
# Copyright (c) Tiago Montes.
# See LICENSE for details.
# ----------------------------------------------------------------------------

import unittest

from aturtle.shapes import vector



class TestBadShapeCreation(unittest.TestCase):

    def test_create_with_bad_typed_coords_raises_TypeError(self):

        bad_values = (None, 42, 'hi', (i for i in range(10)))

        for bad_value in bad_values:
            with self.subTest(bad_value=bad_value):
                with self.assertRaises(TypeError):
                    _shape = vector.Shape(coords=bad_value)


    def test_create_with_odd_number_of_coords_raises_ValueError(self):

        with self.assertRaises(ValueError):
            _shape = vector.Shape([1, 2, 3])



class TestShapeAttributes(unittest.TestCase):

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



class _Base(unittest.TestCase):

    def assert_equal_rounded_list_values(self, list_a, list_b):

        for a, b in zip(list_a, list_b):
            self.assertEqual(round(a), round(b))



class TestShapeAccess(_Base):

    def test_shape_at_angle_0_has_source_coords(self):

        coords = [0, 0, 2, 0, 1, 1]
        shape = vector.Shape(coords)

        result = shape[0]
        self.assert_equal_rounded_list_values(result, coords)


    def test_shape_coords_at_angle_90(self):

        shape = vector.Shape([0, 0, 2, 0, 1, 1])

        result = shape[90]
        self.assert_equal_rounded_list_values(result, [0, 0, 0, 2, -1, 1])


    def test_shape_coords_at_angle_180(self):

        shape = vector.Shape([0, 0, 2, 0, 1, 1])

        result = shape[180]
        self.assert_equal_rounded_list_values(result, [0, 0, -2, 0, -1, -1])


    def test_shape_coords_at_angle_270(self):

        shape = vector.Shape([0, 0, 2, 0, 1, 1])

        result = shape[270]
        self.assert_equal_rounded_list_values(result, [0, 0, 0, -2, 1, -1])



class TestBadRegularPolygonCreation(unittest.TestCase):

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



class TestRegularPolygonAccess(_Base):

    def test_4_sided_polygon_at_angle_0(self):

        shape = vector.RegularPolygon(sides=4, radius=10, angle=0)

        coords = shape[0]
        self.assert_equal_rounded_list_values(
            coords,
            [10, 0, 0, 10, -10, 0, 0, -10],
        )


    def test_4_sided_polygon_at_angle_45(self):

        shape = vector.RegularPolygon(sides=4, side=10, angle=45)

        coords = shape[0]
        self.assert_equal_rounded_list_values(
            coords,
            [5, -5, 5, 5, -5, 5, -5, -5],
        )



class TestSquare(_Base):

    def test_create(self):

        shape = vector.Square()


    def test_default_coords(self):

        shape = vector.Square()
        self.assert_equal_rounded_list_values(
            shape[0],
            [30, -30, 30, 30, -30, 30, -30, -30],
        )


    def test_default_anchor(self):

        shape = vector.Square()
        self.assertEqual(shape.anchor, (0, 0))


    def test_custom_size_coords(self):

        shape = vector.Square(side=42)
        self.assert_equal_rounded_list_values(
            shape[0],
            [21, -21, 21, 21, -21, 21, -21, -21]
        )


    def test_custom_size_anchor(self):

        shape = vector.Square(side=42)
        self.assertEqual(shape.anchor, (0, 0))
