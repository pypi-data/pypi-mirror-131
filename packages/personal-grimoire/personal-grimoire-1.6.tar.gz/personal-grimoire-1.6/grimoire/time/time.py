#!/usr/bin/env python

from datetime import date, datetime, time, timedelta


def date_from_str(datetime):
    return Date.from_str(datetime)


def today_str():
    return Date().today_str()


def now_str(format=None, datetime_format=False):
    return Date.now_str(format, datetime_format)


class Date:
    DATETIME_DEFAULT_FORMAT = "%Y-%m-%d %H:%M:%S"
    DATETIME_DEFULAT_FORMAT_FOR_FILE = "%Y-%m-%d_%H:%M:%S"
    DATE_DEFAULT_FORMAT = "%Y-%m-%d"

    current_format = DATETIME_DEFAULT_FORMAT

    @staticmethod
    def to_str(date, format=None, datetime_format=False) -> str:

        if not format:
            format = Date.DATE_DEFAULT_FORMAT

        if datetime_format:
            format = Date.DATETIME_DEFAULT_FORMAT

        return date.strftime(format)

    def today_str(self):
        return date.today().strftime(Date.DATE_DEFAULT_FORMAT)

    @staticmethod
    def from_str(date):
        return datetime.strptime(date, Date.DATETIME_DEFAULT_FORMAT)

    @staticmethod
    def now_str(format=None, datetime_format=False):
        if not format:
            format = Date.current_format

        if datetime_format:
            format = Date.DATETIME_DEFAULT_FORMAT

        return Date.to_str(datetime.now(), format)

    @staticmethod
    def now():
        return datetime.now()

    @staticmethod
    def datetime_from_str(date):
        return datetime.strptime(date, Date.DATETIME_DEFAULT_FORMAT)

    @staticmethod
    def date_from_str(string):
        return datetime.strptime(string, Date.DATE_DEFAULT_FORMAT)

    @staticmethod
    def yesterday():
        return datetime.now() - timedelta(days=1)

    @staticmethod
    def yesterday_str():
        return Date.yesterday().strftime(Date.DATE_DEFAULT_FORMAT)

    @staticmethod
    def date_to_datetime(date):
        return datetime.combine(date, time(0, 0))

    @staticmethod
    def parse_str(string):
        return Parser.from_str(string)


class Parser:
    @staticmethod
    def from_str(string) -> str:

        if string == "yesterday" or string == "yes":
            return Date.yesterday().strftime(Date.DATE_DEFAULT_FORMAT)

        if string == "now":
            return Date.now_str()

        import dateparser

        parsed = dateparser.parse(string)
        if not parsed:
            raise Exception(f"Could not parse string to date {string}")

        return parsed.strftime(Date.DATE_DEFAULT_FORMAT)


if __name__ == "__main__":
    import fire

    fire.Fire(Date)
