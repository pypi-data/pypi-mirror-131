import gc
import logging
import sys
import time
from functools import wraps


def obj_size(obj):
    marked = {id(obj)}
    obj_q = [obj]
    sz = 0

    while obj_q:
        sz += sum(map(sys.getsizeof, obj_q))

        # Lookup all the object referred to by the object in obj_q.
        # See: https://docs.python.org/3.7/library/gc.html#gc.get_referents
        all_refr = ((id(o), o) for o in gc.get_referents(*obj_q))

        # Filter object that are already marked.
        # Using dict notation will prevent repeated objects.
        new_refr = {
            o_id: o
            for o_id, o in all_refr
            if o_id not in marked and not isinstance(o, type)
        }

        # The new obj_q will be the ones that were not marked,
        # and we will update marked with their ids so we will
        # not traverse them again.
        obj_q = new_refr.values()
        marked.update(new_refr.keys())

    return sz


def execution_time(f, *args, **kwargs):
    """
    Use me like:

    grimoire.execution_time(time.sleep, 3)
    """
    log_and_print(f"Starting to measure time")
    t0 = time.time()
    result = f(*args, **kwargs)
    t1 = time.time()
    log_and_print(f"Seconds ellapsed between beginning and end: {t1 - t0}")

    return result


def time_to_execute_wraper(func):
    @wraps(func)
    def internal_decorator(*args, **kwargs):
        return execution_time(func, *args, *kwargs)

    return internal_decorator


def log_and_print(message):
    logging.info(message)
    print(message)


def log_request(logger, request):
    """ logs a flask web request """
    body = "HTTP URL: {0} HTTP HEADERS: {1} HTTP BODY: {2}".format(
        request.url, request.headers, request.get_json()
    )
    logger.log(body)


def log_io_wrapper(func):
    @wraps(func)
    def internal_decorator(*args, **kwargs):
        logging.info(f"Input: args {args}, kargs {kwargs}")
        result = func(*args, **kwargs)
        logging.info(f"Output: {result}")
        return result

    return internal_decorator
