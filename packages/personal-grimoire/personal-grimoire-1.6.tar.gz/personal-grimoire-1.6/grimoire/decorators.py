import logging
import sys
import time
from functools import wraps

from grimoire.notification import send_notification, send_error_message


def log_exception():
    def _(func):
        @wraps(func)
        def __(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
            except Exception as e:
                exception_type, exception_object, exception_traceback = sys.exc_info()
                filename = exception_traceback.tb_frame.f_code.co_filename
                line_number = exception_traceback.tb_lineno
                error_str = str(e)
                logging_string = f"{error_str}|File: {filename}|Line: {line_number}|"
                logging.error(logging_string)
                send_notification(f"error {logging_string}")
                raise e
            return result

        return __

    return _


def notify_exception():
    """
    Will let you know when a function is called or returned error as a desktop notification
    """

    def _(func):
        @wraps(func)
        def __(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
            except Exception as e:
                send_notification(f"Failed {func.__name__} error: {str(e)}")
                raise e
            return result

        return __

    return _

def notify_exception_i3(*args, **kwargs):
    def _(func):
        @wraps(func)
        def __(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
            except Exception as e:
                send_error_message(f"Exception {e}")
                raise e
            return result

        return __

    return _



def notify_execution():
    """
    Will let you know when a function is called or returned error as a desktop notification
    """

    def _(func):
        @wraps(func)
        def __(*args, **kwargs):
            try:
                send_notification(f"Started {func.__name__} execution")
                result = func(*args, **kwargs)
            except Exception as e:
                send_notification(f"Failed {func.__name__} error: {str(e)}")
                raise e

            send_notification(f"Successful {func.__name__} execution")
            return result

        return __

    return _


def log_request(logger, request):
    """ logs a flask web request """
    body = "HTTP URL: {0} HTTP HEADERS: {1} HTTP BODY: {2}".format(
        request.url, request.headers, request.get_json()
    )
    logger.log(body)


def collect_requests_count(identifier: str, statsd):
    def monitor_requests_decorator(func):
        @wraps(func)
        def internal_decorator(*args, **kwargs):
            result = func(*args, **kwargs)
            statsd.increment(identifier)
            return result

        return internal_decorator

    return monitor_requests_decorator


def monitor_empty_result(statsd, sentry_logger, datadog_id, message, func):
    @wraps(func)
    def internal_decorator(*args, **kwargs):
        result = func(*args, **kwargs)
        if not result:
            statsd.increment(datadog_id)
            sentry_logger.captureMessage(message.format(args[0], args[2]))
        return result

    return internal_decorator


def collect_execution_time(identifier: str, statsd):
    """ calls the wraped function  and send the execution time to statsd with the given identifier """

    def monitor_time_decorator(func):
        @wraps(func)
        def internal_decorator(*args, **kwargs):
            overall_start_time = time.time()
            result = func(*args, **kwargs)
            statsd.histogram(identifier, round(time.time() - overall_start_time, 4))
            return result

        return internal_decorator

    return monitor_time_decorator


def log_call(func):
    """wrapps a function call providing a string message with placeholders for arguments and result
    use like this:
    converter._perform_request = log_function_call(di.logger(), func, "Calling price converter api \nARGs: {} \nRESULT: {} ")
    """

    @wraps(func)
    def internal_decorator(*args, **kwargs):
        result = func(*args, **kwargs)
        logging.info(
            f"Call function ({func.__name__}) with arguments ({args}), and result: {result}"
        )
        return result

    return internal_decorator
