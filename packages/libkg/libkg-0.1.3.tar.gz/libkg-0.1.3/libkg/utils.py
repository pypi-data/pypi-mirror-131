import traceback


def catch_exception(function):
    """
    a decorator to catch exception and print it.
    :return:
    """
    # todo: make this print as the parameter of the decorator
    def wrapped(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except Exception as err:
            traceback.print_exc()

    return wrapped
