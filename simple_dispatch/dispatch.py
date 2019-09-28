from typing import Callable

_handlers = None


def connect(event_name: str, func: Callable):
    """
    Connects a given function to be subscribed to the given event.

    :param event_name: The name of the event to subscribe to.
    :param func: The function that will be invoked when the event is published.
    """
    global _handlers

    # If we have not defined handlers, define them.
    if not _handlers:
        _handlers = dict()

    # If this is the first handler for the function, create a list of just the one handler.
    # Otherwise, append a new handler to the existing list.
    if event_name not in _handlers:
        _handlers[event_name] = [func]
    else:
        _handlers[event_name].append(func)


def dispatch(event_name: str, **kwargs):
    """
    Dispatches a particular event to all subscribers with the given arguments. The subscribers
    are assumed to accept kwargs. If not, an error will be incurred.

    :param event_name: The name of the event that is being published.
    :param kwargs: The arguments to pass to the handler functions.
    """
    global _handlers
    # If no handlers, quit early.
    if not _handlers or event_name not in _handlers:
        return

    for handler in _handlers[event_name]:
        handler(**kwargs)


def subscriber(*args):
    """
    Subscribes the annotated callable to one or more events. You can either pass a single or more than one
    event to this annotation

    :param args: The list of hashable event declarations that we are going to subscribe to.
    """
    def decorator(func):
        for event in args:
            connect(event, func)

        return func

    return decorator


def dispatch_before(event_name):
    """
    Dispatches the defined event before the function is executed. args and kwargs are passed to the handler.

    @subscriber('BEFORE_SOME_EVENT')
    def my_handler(**kwargs):
        caller_args = kwargs['func_args']
        caller_kwargs = kwargs['func_kwargs']

    :param event_name: The name of the event to dispatch.
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            dispatch(event_name, func_args=args, func_kwargs=kwargs)
            return func(*args, **kwargs)

        return wrapper

    return decorator


def dispatch_after(event_name):
    """
    Dispatches the defined event after the function is executed and before the result is returned to the caller of the
    annotated function. Additionally, the result or return of the function call is passed in the result kwarg.

     @subscriber('AFTER_SOME_EVENT')
     def my_handler(**kwargs):
        caller_args = kwargs['func_args']
        caller_kwargs = kwargs['func_kwargs']
        caller_result = kwargs['result']

    :param event_name: The name of the event to dispatch.
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            dispatch(event_name, func_args=args, func_kwargs=kwargs, result=result)
            return result

        return wrapper

    return decorator
