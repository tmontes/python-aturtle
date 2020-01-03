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
        if bitmap.tkinter:
            # PIL is not available: force PIL codepath, nonetheless.
            self.saved_tkinter = bitmap.tkinter
            bitmap.tkinter = None
        else:
            self.saved_tkinter = None
        # PIL codepath tests run against fake_pil.
        self.save_pil_image = bitmap.Image
        self.save_pil_image_tk = bitmap.ImageTk
        self.pil_image = fake_pil.FakePILImage
        self.pil_image_tk = fake_pil.FakePILImageTk
        bitmap.Image = self.pil_image
        bitmap.ImageTk = self.pil_image_tk

    def tearDown(self):
        self.pil_image.reset_after_tests()
        bitmap.Image = self.save_pil_image
        bitmap.ImageTk = self.save_pil_image_tk
        if self.saved_tkinter:
            bitmap.tkinter = self.saved_tkinter



class _TkBasedTests(unittest.TestCase):

    def setUp(self):
        if not bitmap.tkinter:
            # PIL is available: force tkinter code paths with fake_tkinter.
            self.tkinter = fake_tkinter.FakeTkinter(640, 480)
            bitmap.tkinter = self.tkinter
        else:
            self.tkinter = None


    def tearDown(self):
        if self.tkinter:
            bitmap.tkinter = None



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
