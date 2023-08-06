import logging
import os
import sys
import traceback
from enum import Enum
from functools import wraps

import sentry_sdk

from grimoire.current_enviroment import CurrentEnvironment
from grimoire.notification import send_error_message, send_notification


class LogLevel(str, Enum):
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"


class Error:
    title = "Unamed Generic Error"
    http_status = 500
    log_level = LogLevel.ERROR
    line = 0
    file = ""
    trace = None

    @staticmethod
    def _from_exception(exception):
        error = Error()
        error.http_status = exception.code if hasattr(exception, "code") else 500
        error.title = str(exception)
        error.log_level = (
            exception.log_level if hasattr(exception, "log_level") else LogLevel.ERROR
        )

        return error

    def serialize(self):
        return self.__dict__


class ErrorHandler:
    sentry_enabled = False

    @staticmethod
    def enable_sentry():
        import sentry_sdk

        sentry_sdk.init(
            "https://1030b88890e54879a61904ffb59e5acb@o473103.ingest.sentry.io/5507665",
            traces_sample_rate=1.0,
        )

    def handle_and_retrow(self, exception):
        self.handle(exception)
        raise exception

    def handle(self, exception: Exception):
        """
         Exceptions can be configured by passing a config attribute to them

        Example:
        class AnkiException(Exception):
            config = {
                "disable_tray_message": True,
                "enable_notification": True,
                "disable_sentry": True,
            }

        """

        # the fire library throws an exception with code=0 when one uses it to ask for manual
        # it is an desireable behaviour so we should not treat it as an error
        from fire.core import FireExit

        if isinstance(exception, FireExit) and exception.code == 0:
            return

        exc_info = sys.exc_info()  # type: ignore

        logging.debug("".join(traceback.format_exception(*exc_info)))
        if not ErrorHandler.sentry_enabled:
            ErrorHandler.enable_sentry()

        if CurrentEnvironment().is_local():
            self._show_tray(exception, exc_info)

            if self.exception_has_config(exception, "enable_notification"):
                send_notification(str(exception), urgent=True)

            if not self.exception_has_config(exception, "disable_sentry"):
                sentry_sdk.capture_exception(exception)

    def exception_has_config(self, exception, config_name):
        if hasattr(exception, "config") and config_name in exception.config:
            return exception.config[config_name]

        return False

    def _show_tray(self, exception, exc_info):
        file_name = os.path.split(exc_info[2].tb_frame.f_code.co_filename)[1]  # type: ignore
        line_number = exc_info[2].tb_lineno  # type: ignore
        if not self.exception_has_config(exception, "disable_tray_message"):
            send_error_message(
                f"Exception: {str(exception)}, file: {file_name}, line: {line_number}",
                (
                    "Open sentry",
                    "browser 'https://sentry.io/organizations/jena-machado/issues/?project=5507665'",
                ),
            )

    @staticmethod
    def handle_with_context(context):
        def error_handler_decorator(func):
            @wraps(func)
            def internal_error_handler(*args, **kwargs):
                result = None
                try:
                    result = func(*args, **kwargs)
                    return result
                except BaseException as e:
                    ErrorHandler().handle(e, context)

                    raise e

            return internal_error_handler

        return error_handler_decorator

    @staticmethod
    def exception_to_entity(exception: Exception) -> Error:
        return Error._from_exception(exception)
