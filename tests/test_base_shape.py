# ----------------------------------------------------------------------------
# Python A-Turtle
# ----------------------------------------------------------------------------
# Copyright (c) Tiago Montes.
# See LICENSE for details.
# ----------------------------------------------------------------------------

import unittest

from aturtle.shapes import base



class TestDirectInstatiation(unittest.TestCase):

    def test_instantiation_raises_NotImplemented(self):

        with self.assertRaises(NotImplementedError):
            _shape = base.Shape(image='image', anchor=(0, 0), rotations=8)



class _TestShape(base.Shape):

    def __init__(self, *args, **kwargs):
        self.rotated_data_calls = []
        super().__init__(*args, **kwargs)

    def rotated_data(self, image, around, step, rotations):
        result = (image, around, step, rotations)
        self.rotated_data_calls.append(result)
        return result



class TestCreateWithBadArguments(unittest.TestCase):

    def test_non_tuple_or_list_anchor_raises_TypeError(self):

        bad_anchors = (None, 42, 'hi', (1 for _ in range(2)))
        for bad_anchor in bad_anchors:
            with self.subTest(bad_anchor=bad_anchor):
                with self.assertRaises(TypeError):
                    _shape = _TestShape(image=None, anchor=bad_anchor, rotations=1)


    def test_negative_rotations_raises_ValueError(self):

        with self.assertRaises(ValueError):
            shape = _TestShape(image=None, anchor=(0, 0), rotations=-1)


    def test_zero_rotations_raises_ValueError(self):

        with self.assertRaises(ValueError):
            shape = _TestShape(image=None, anchor=(0, 0), rotations=0)



class TestCreatePreRotateDefault(unittest.TestCase):

    def test_create_calls_rotated_data_once_per_rotation(self):

        for rotations in (1, 4, 8, 36, 72, 360):
            with self.subTest(rotations=rotations):
                shape = _TestShape(image='image', anchor=(0, 0), rotations=rotations)
                self.assertEqual(len(shape.rotated_data_calls), rotations)


    def test_create_calls_rotated_data_with_the_passed_in_image(self):

        image = 'the-image'
        shape = _TestShape(image=image, anchor=(0, 0), rotations=4)
        for passed_image, _anchor, _step, _rotations in shape.rotated_data_calls:
            self.assertEqual(passed_image, image)


    def test_create_calls_rotated_data_with_the_passed_in_anchor(self):

        anchor = (24, 42)
        shape = _TestShape(image='image', anchor=anchor, rotations=4)
        for _image, passed_anchor, _step, _rotations in shape.rotated_data_calls:
            self.assertEqual(passed_anchor, anchor)


    def test_create_calls_rotated_data_once_per_range_of_steps(self):

        rotations = 42
        shape = _TestShape(image='image', anchor=(0, 0), rotations=rotations)
        passed_steps = [
            passed_step
            for _image, _anchor, passed_step, _rotations in shape.rotated_data_calls
        ]
        self.assertEqual(passed_steps, list(range(rotations)))


    def test_create_calls_rotated_data_with_the_passed_in_rotations(self):

        rotations = 24
        shape = _TestShape(image='image', anchor=(0, 0), rotations=rotations)
        for _image, _anchor, _step, passed_rotations in shape.rotated_data_calls:
            self.assertEqual(passed_rotations, rotations)



class TestCreatePreRotateFalse(unittest.TestCase):

    def test_create_does_not_call_rotated_data(self):

        shape = _TestShape(image='image', anchor=(0, 0), rotations=8, pre_rotate=False)
        self.assertFalse(shape.rotated_data_calls)




class TestAccessPreRotateDefault(unittest.TestCase):

    def test_angle_0_is_rotated_data_at_step_0(self):

        shape = _TestShape(image='image', anchor=(0, 0), rotations=72)

        image = shape[0]
        (_image, _anchor, step, _rotations) = image
        self.assertEqual(step, 0)


    def test_angle_90_is_rotated_data_at_step_9_out_of_36(self):

        shape = _TestShape(image='image', anchor=(0, 0), rotations=36)

        image = shape[90]
        (_image, _anchor, step, _rotations) = image
        self.assertEqual(step, 9)


    def test_angle_180_is_rotated_data_at_step_4_out_of_8(self):

        shape = _TestShape(image='image', anchor=(0, 0), rotations=8)

        image = shape[180]
        (_image, _anchor, step, _rotations) = image
        self.assertEqual(step, 4)


    def test_angle_270_5_is_rotated_data_at_step_2705_out_of_3600(self):

        shape = _TestShape(image='image', anchor=(0, 0), rotations=3600)

        image = shape[270.5]
        (_image, _anchor, step, _rotations) = image
        self.assertEqual(step, 2705)


    def test_acessing_all_angles_does_not_call_rotated_data(self):

        shape = _TestShape(image='image', anchor=(0, 0), rotations=360)
        call_count_before = len(shape.rotated_data_calls)

        for angle in range(360):
            _result = shape[angle]

        call_count_after = len(shape.rotated_data_calls)
        self.assertEqual(call_count_before, call_count_after)



class TestAccessPreRotateFalse(unittest.TestCase):

    def _create_shape(self, image, anchor, rotations):

        return _TestShape(
            image=image,
            anchor=anchor,
            rotations=rotations,
            pre_rotate=False,
        )

    def test_one_access_calls_rotated_data_once(self):

        image = 'image'
        shape = self._create_shape(image=image, anchor=(0, 0), rotations=8)
        self.assertFalse(shape.rotated_data_calls)

        _result = shape[0]
        self.assertEqual(len(shape.rotated_data_calls), 1)


    def test_one_access_calls_rotated_data_with_passed_image(self):

        image = 'the-image'
        shape = self._create_shape(image=image, anchor=(0, 0), rotations=8)
        self.assertFalse(shape.rotated_data_calls)

        _result = shape[0]
        [(passed_image, _anchor, _step, _rotations)] = shape.rotated_data_calls
        self.assertEqual(passed_image, image)


    def test_one_access_calls_rotated_data_with_passed_anchor(self):

        anchor = (24, 42)
        shape = self._create_shape(image='image', anchor=anchor, rotations=8)
        self.assertFalse(shape.rotated_data_calls)

        _result = shape[0]
        [(_image, passed_anchor, _step, _rotations)] = shape.rotated_data_calls
        self.assertEqual(passed_anchor, anchor)


    def test_one_access_calls_rotated_data_with_passed_rotations(self):

        rotations = 24
        shape = self._create_shape(image='image', anchor=(0, 0), rotations=rotations)
        self.assertFalse(shape.rotated_data_calls)

        _result = shape[0]
        [(_image, _anchor, _step, passed_rotations)] = shape.rotated_data_calls
        self.assertEqual(passed_rotations, rotations)


    def test_access_angle_0_calls_rotated_data_with_step_0(self):

        shape = self._create_shape(image='image', anchor=(0, 0), rotations=8)
        self.assertFalse(shape.rotated_data_calls)

        _result = shape[0]
        [(_image, _anchor, passed_step, _rotations)] = shape.rotated_data_calls
        self.assertEqual(passed_step, 0)


    def test_acessing_all_angles_calls_rotated_data_rotations_times(self):

        rotations = 8
        shape = self._create_shape(image='image', anchor=(0, 0), rotations=rotations)
        self.assertFalse(shape.rotated_data_calls)

        for angle in range(360):
            _result = shape[angle]

        self.assertEqual(len(shape.rotated_data_calls), rotations)



class TestAttributes(unittest.TestCase):

    def test_pre_rotate_default_anchor_attribute(self):

        anchor = (42, 24)
        shape = _TestShape(image='image', anchor=anchor, rotations=1)

        self.assertEqual(shape.anchor, anchor)


    def test_pre_rotate_False_anchor_attribute(self):

        anchor = (42, 24)
        shape = _TestShape(image='image', anchor=anchor, rotations=1, pre_rotate=False)

        self.assertEqual(shape.anchor, anchor)
