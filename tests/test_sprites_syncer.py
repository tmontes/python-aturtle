# ----------------------------------------------------------------------------
# Python A-Turtle
# ----------------------------------------------------------------------------
# Copyright (c) Tiago Montes.
# See LICENSE for details.
# ----------------------------------------------------------------------------

import asyncio
import unittest
from unittest import mock

from aturtle.sprites import syncer



class Test(unittest.TestCase):

    def test_syncer_raises_TypeError_with_regular_func(self):

        def sync_func():
            pass

        with self.assertRaises(TypeError):
            _result = syncer.create_sync_func(sync_func, lambda n: n)


    def test_syncer_converts_await_asyncio_sleep_to_time_sleep(self):

        async def async_sleep():
            await asyncio.sleep(42)

        sync_sleep = syncer.create_sync_func(async_sleep, lambda n: n)

        # The `time` module was injected into the function globals.
        time_module_mock = mock.Mock()
        with mock.patch(__name__ + '.time', time_module_mock):
            sync_sleep()

        # `time.sleep(42)` was called.
        time_module_mock.sleep.assert_called_once_with(42)


    def test_syncer_handles_using_default_kwargs(self):

        async def async_sleep(*, duration=42):
            await asyncio.sleep(duration)

        sync_sleep = syncer.create_sync_func(async_sleep, lambda n: n)

        # The `time` module was injected into the function globals.
        time_module_mock = mock.Mock()
        with mock.patch(__name__ + '.time', time_module_mock):
            sync_sleep()

        # `time.sleep(42)` was called.
        time_module_mock.sleep.assert_called_once_with(42)


    def test_syncer_handles_overriding_default_kwargs(self):

        async def async_sleep(*, duration=42):
            await asyncio.sleep(duration)

        sync_sleep = syncer.create_sync_func(async_sleep, lambda n: n)

        # The `time` module was injected into the function globals.
        time_module_mock = mock.Mock()
        with mock.patch(__name__ + '.time', time_module_mock):
            sync_sleep(duration=24)

        # `time.sleep(24)` was called.
        time_module_mock.sleep.assert_called_once_with(24)


    def test_syncer_converts_awaited_self_references(self):

        class Async:
            async def async_sleep(self, duration):
                await asyncio.sleep(duration)
            async def async_repeat(self, duration, times):
                for _ in range(times):
                    await self.async_sleep(duration)

            sync_sleep = syncer.create_sync_func(async_sleep, lambda n: n[1:])
            sync_repeat = syncer.create_sync_func(async_repeat, lambda n: n[1:])

        a = Async()

        # The `time` module was injected into the method globals.
        time_module_mock = mock.Mock()
        with mock.patch(__name__ + '.time', time_module_mock):
            a.sync_repeat(7, 42)

        # `time.sleep` was called 42 times..
        time_sleep_call_args_list = time_module_mock.sleep.call_args_list
        self.assertEqual(len(time_sleep_call_args_list), 42, 'time.sleep call count')

        # `time.sleep` was always called with a single positional argument: 7.
        for time_sleep_call_args in time_sleep_call_args_list:
            self.assertEqual(time_sleep_call_args, mock.call(7))

