from simple_dispatch import connect, subscriber, dispatch

from unittest import TestCase


class TestCases(TestCase):
    def test_subscription(self):
        """
        There are a few test functions defined. One that subscribes to event A. One that subscribes to event B, and
        a third that subscribes to both. Make sure the right functions are called at the right time.
        """
        EVENT_A = 'A'
        EVENT_B = 'B'

        # Before handlers are defined should not error
        dispatch(EVENT_A, a=True, b=False)

        @subscriber(EVENT_A)
        def sub_a(**kwargs):
            self.assertTrue(kwargs['a'])
            self.assertFalse(kwargs['b'])

        @subscriber(EVENT_B)
        def sub_b(**kwargs):
            self.assertFalse(kwargs['a'])
            self.assertTrue(kwargs['b'])

        @subscriber(EVENT_A, EVENT_B)
        def sub_both(**kwargs):
            self.assertNotEqual(kwargs['a'], kwargs['b'])

        dispatch(EVENT_A, a=True, b=False)
        dispatch(EVENT_B, a=False, b=True)