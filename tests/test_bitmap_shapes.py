# ----------------------------------------------------------------------------
# Python A-Turtle
# ----------------------------------------------------------------------------
# Copyright (c) Tiago Montes.
# See LICENSE for details.
# ----------------------------------------------------------------------------

import base64
import unittest

from aturtle.shapes import bitmap

from . import fake_pil
from . import fake_tkinter



class _PILBasedTests(unittest.TestCase):

    def setUp(self):

        # PIL code path tests run against fake_pil objects.
        self.pil_image = fake_pil.PILImage
        self.pil_image_tk = fake_pil.PILImageTk()

        if bitmap.tkinter:
            self.save_pil_image = None
            self.save_pil_image_tk = None
        else:
            self.save_pil_image = bitmap.Image
            self.save_pil_image_tk = bitmap.ImageTk

        # Force PIL code path.
        self.save_tkinter = bitmap.tkinter
        bitmap.tkinter = None

        # Replace PIL objects with fake ones.
        bitmap.Image = self.pil_image
        bitmap.ImageTk = self.pil_image_tk


    def tearDown(self):

        self.pil_image.reset_after_tests()

        # Restore PIL objects in module, or remove them.
        bitmap.Image = self.save_pil_image
        if not self.save_pil_image:
            del bitmap.Image
        bitmap.ImageTk = self.save_pil_image_tk
        if not self.save_pil_image_tk:
            del bitmap.ImageTk

        # Restore the module's tkinter reference.
        bitmap.tkinter = self.save_tkinter



class _TkBasedTests(unittest.TestCase):

    def setUp(self):

        # PIL code path tests run against fake_tkinter.
        self.tkinter = fake_tkinter.Module(640, 480)

        # Replace tkinter with the fake one.
        self.save_tkinter = bitmap.tkinter
        bitmap.tkinter = self.tkinter


    def tearDown(self):

        # Restore the module's tkinter reference.
        bitmap.tkinter = self.save_tkinter



class _BadShapeCreationMixin:

    def test_create_with_no_filename_or_data_raises_ValueError(self):

        with self.assertRaises(ValueError):
            _shape = bitmap.Shape()


    def test_create_with_empty_filename_raises(self):

        with self.assertRaises(ValueError):
            _shape = bitmap.Shape(filename='')


    def test_create_with_empty_data_raises(self):

        with self.assertRaises(ValueError):
            _shape = bitmap.Shape(data=b'')


class TestBadShapeCreationTk(_TkBasedTests, _BadShapeCreationMixin):
    pass

class TestBadShapeCreationPIL(_PILBasedTests, _BadShapeCreationMixin):
    pass



class TestShapeCreationNoPreRotateTk(_TkBasedTests):

    def test_create_with_filename_creates_one_tkinter_PhotoImage(self):

        _shape = bitmap.Shape(filename='the-filename', pre_rotate=False)

        photoimage_init_calls = self.tkinter.photoimage_init_calls
        self.assertEqual(len(photoimage_init_calls), 1)


    def test_create_with_data_creates_one_tkinter_PhotoImage(self):

        _shape = bitmap.Shape(data=b'some-data', pre_rotate=False)

        photoimage_init_calls = self.tkinter.photoimage_init_calls
        self.assertEqual(len(photoimage_init_calls), 1)


    def test_create_with_filename_passes_it_as_file_to_PhotoImage(self):

        filename = 'the-filename'
        _shape = bitmap.Shape(filename=filename, pre_rotate=False)

        photoimage_init_calls = self.tkinter.photoimage_init_calls
        [_first_call_args, first_call_kwargs], *_ = photoimage_init_calls
        self.assertEqual(first_call_kwargs['file'], filename)


    def test_create_with_data_passes_it_as_data_to_PhotoImage(self):

        data = b'some-data'
        _shape = bitmap.Shape(data=data, pre_rotate=False)

        photoimage_init_calls = self.tkinter.photoimage_init_calls
        [_first_call_args, first_call_kwargs], *_ = photoimage_init_calls
        self.assertEqual(first_call_kwargs['data'], data)



class TestShapeCreationNoPreRotatePIL(_PILBasedTests):

    def test_create_with_filename_creates_one_PIL_Image(self):

        _shape = bitmap.Shape(filename='the-filename', pre_rotate=False)

        image_init_calls = self.pil_image.init_calls
        self.assertEqual(len(image_init_calls), 1)


    def test_create_with_data_creates_one_PIL_Image(self):

        _shape = bitmap.Shape(data=b'some-data', pre_rotate=False)

        image_init_calls = self.pil_image.init_calls
        self.assertEqual(len(image_init_calls), 1)


    def test_create_with_filename_passes_it_to_PIL_Image(self):

        filename = 'the-filename'
        _shape = bitmap.Shape(filename=filename, pre_rotate=False)

        image_init_calls = self.pil_image.init_calls
        [first_call_args, _first_call_kwargs], *_ = image_init_calls
        self.assertEqual(first_call_args[0], filename)


    def test_create_with_data_b64decodes_and_passes_as_file_to_PIL_Image(self):

        binay_data = b'hello there'
        b64data = base64.b64encode(binay_data)
        _shape = bitmap.Shape(data=b64data, pre_rotate=False)

        image_init_calls = self.pil_image.init_calls
        [first_call_args, _first_call_kwargs], *_ = image_init_calls
        first_call_first_arg, *_ = first_call_args
        file_data = first_call_first_arg.read()

        self.assertEqual(file_data, binay_data)



class TestShapeCreationPreRotateTk(_TkBasedTests):

    def test_create_generates_rotation_minus_one_PhotoImage_copies(self):

        rotations = 8
        shape = bitmap.Shape(filename='filename', rotations=rotations)
        straight = shape[0]

        self.assertEqual(straight.copies, rotations-1)


    def test_copy_creation_calls_PhotoImage_get_and_transparency_get(self):

        rotations = 2
        shape = bitmap.Shape(filename='filename', rotations=rotations)
        straight = shape[0]

        # PhotoImage.get and .transparency_get called:
        # - More than once...
        # - ...and, at most, width x height x (rotations - 1).
        max_calls = straight.width() * straight.height() * (rotations-1)
        get_calls = straight.get.call_count
        self.assertGreater(get_calls, 0)
        self.assertLessEqual(get_calls, max_calls)


    def test_copy_creation_calls_PhotoImage_put_and_transparency_set(self):

        rotations = 2
        shape = bitmap.Shape(filename='filename', rotations=rotations)
        inverted = shape[180]

        # PhotoImage.put called once.
        # PhotoImage.transparency_set called width x height.
        self.assertEqual(inverted.put.call_count, 1)
        tset_calls = inverted.width() * inverted.height()
        self.assertEqual(inverted.transparency_set.call_count, tset_calls)



class TestShapeCreationPreRotatePIL(_PILBasedTests):

    def test_create_leads_to_rotation_PhotoImage_calls(self):

        rotations = 8
        _shape = bitmap.Shape(filename='filename', rotations=rotations)

        self.assertEqual(
            len(self.pil_image_tk.photoimage_calls),
            rotations,
        )


    def test_create_calls_Image_rotate_rotation_minus_one_times(self):

        rotations = 4
        _shape = bitmap.Shape(filename='filename', rotations=rotations)

        self.assertEqual(self.pil_image.rotate.call_count, rotations-1)


class ShapeAnchorTestsMixin:

    def test_int_anchor_is_taken_as_is(self):

        anchor = (20, 10)
        shape = bitmap.Shape(filename='filename', anchor=anchor, pre_rotate=False)
        self.assertEqual(shape.anchor, anchor)


    def test_float_anchor_is_relative_to_width_height(self):

        anchor = (0.5, 0.5)
        shape = bitmap.Shape(filename='filename', anchor=anchor, pre_rotate=False)

        # The underlying fake images are 42 x 24.
        expected_anchor = (21, 12)
        self.assertEqual(shape.anchor, expected_anchor)


class TestShapeAnchorTestsTk(_TkBasedTests, ShapeAnchorTestsMixin):
    pass

class TestShapeAnchorTestsPIL(_PILBasedTests, ShapeAnchorTestsMixin):
    pass
