import functools
import time


def timed(fn):
    @functools.wraps(fn)
    def inner(*args, **kwargs):
        started_at = time.time()
        result = fn(*args, **kwargs)
        duration = time.time() - started_at
        print(f"{fn.__name__} took {duration:.3f}")
        return result

    return inner
