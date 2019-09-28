from simple_dispatch import subscriber, dispatch, dispatch_after, dispatch_before

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

    def test_before_after(self):
        EVENT_BEFORE = 'BEFORE_A'
        EVENT_AFTER = 'BEFORE_B'

        @subscriber(EVENT_BEFORE)
        def before_some_event(**kwargs):
            caller_args = kwargs['func_args']
            caller_kwargs = kwargs['func_kwargs']

            self.assertEqual(caller_args, (1, 2))
            self.assertEqual(caller_kwargs, {'something_else': True})

        @subscriber(EVENT_AFTER)
        def after_some_event(**kwargs):
            caller_args = kwargs['func_args']
            caller_kwargs = kwargs['func_kwargs']
            caller_result = kwargs['result']

            self.assertEqual(caller_args, (1, 2))
            self.assertEqual(caller_kwargs, {'something_else': True})
            self.assertFalse(caller_result)

        @dispatch_before(EVENT_BEFORE)
        @dispatch_after(EVENT_AFTER)
        def some_event(a, b, something_else=False):
            self.assertEqual([a, b], [1, 2])
            self.assertTrue(something_else)
            return False

        some_event(1, 2, something_else=True)
