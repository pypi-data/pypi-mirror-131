import logging
import logging.config
import re
import sys
from typing import List


class Logger:
    @staticmethod
    def enable_sentry():
        import sentry_sdk

        sentry_sdk.init(
            "https://1030b88890e54879a61904ffb59e5acb@o473103.ingest.sentry.io/5507665",
            traces_sample_rate=1.0,
        )

    def __init__(
        self, config=None, log_file=None, disable_existing=False, file_level="INFO"
    ):

        self.disable_existing = disable_existing
        if log_file:
            self.log_file = log_file
        else:
            self.log_file = "/tmp/default_log"

        self.file_level = file_level

        if not config:
            config = self.default_config()

        logging.config.dictConfig(config)

    def default_config(self):
        return {
            "version": 1,
            "disable_existing_loggers": self.disable_existing,
            "filters": {"exclude_distraction": {"()": _ExcludeWhatIsNotBeingFocused}},
            "formatters": {
                "my_formatter": {
                    "format": '{"level": "%(levelname)s", "message": "%(message)s", "module": "%(module)s", "date": "%(asctime)s", "logger": "%(name)s"}'
                },
                "lean_format": {
                    "format": "%(asctime)s|%(levelname)s|%(message)s|%(module)s|%(name)s",
                    "datefmt": "%Y-%m-%d|%H:%M:%S",
                },
            },
            "handlers": {
                "console_stderr": {
                    "class": "logging.StreamHandler",
                    "level": "ERROR",
                    "formatter": "lean_format",
                    "stream": sys.stderr,
                },
                "console_stdout": {
                    "class": "logging.StreamHandler",
                    "level": "DEBUG",
                    "formatter": "lean_format",
                    "stream": sys.stdout,
                },
                "all_to_file": {
                    "class": "logging.FileHandler",
                    "level": self.file_level,
                    "formatter": "lean_format",
                    "filename": self.log_file,
                },
            },
            "root": {
                # In general, this should be kept at 'NOTSET'.
                # Otherwise it would interfere with the log levels set for each handler.
                "level": "NOTSET",
                "handlers": ["console_stderr", "console_stdout", "all_to_file"],
            },
        }


class _ExcludeWhatIsNotBeingFocused(logging.Filter):
    """_ExcludeWhatIsNotBeingFocused."""

    patterns: List[str] = [
        # ".*kafka.*"
    ]

    def filter(self, record):
        for pattern in self.patterns:
            if re.match(pattern, record.name, re.IGNORECASE):
                return False
        return True
