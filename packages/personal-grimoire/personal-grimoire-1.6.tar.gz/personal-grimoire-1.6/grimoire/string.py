from __future__ import annotations

import logging
import re
from typing import List, Union


def clean_string(x):
    result = StringManipulation.chomp(x)
    result = result.strip()

    return result


def chomp(x):
    """remove special chars from end of string"""
    if x.endswith("\r\n"):
        return x[:-2]
    if x.endswith("\n") or x.endswith("\r"):
        return x[:-1]
    return x


def generate_identifier(string):
    """
    strip the string from all special characters lefting only [A-B-09]
    """
    result = "".join(e for e in string if e.isalnum())
    result = result.lower()

    return result


def everything_after_char(char, string):
    """
    Splits a string by the char and returns everything that comes after the
    first occurence of that char

    """
    return char.join(string.split(char)[1:])


def everything_before_char(char, string):
    """
    Splits a string by the char and returns everything that comes after the
    first occurence of that char

    """
    return string.split(char)[0]


def remove_new_lines(string):
    """
    replaces new lines by spaces
    replaces tabs by none
    :param string:
    :return:
    """
    return string.replace("\n", " ").replace("\r", "")


def quote_with(string, quote_type="'"):
    """
    Quotes a string with the given char.
    If the char is found inside the string replace the content by another quoting char.
    Applies to ' and "

    :param string:
    :param quote_type:
    :return:
    """
    if quote_type is "'":
        return string.replace('"', "'")

    return string.replace("'", '"')


def surround_by_quote(quote_type, string):
    return quote_type + string + quote_type


def remove_chars(string: str, chars: List[str]):
    """
    You specify a list of characters to be removed from given string
    """
    for char in chars:
        string = string.replace(char, "")

    return string


def remove_special_chars(string, exceptions=[]):
    """
    Remove all special chars from strings except if they are one of the exceptions
    """
    result = "".join(e for e in string if e.isalnum() or e in exceptions)
    return result


class Url:
    @staticmethod
    def is_url(result):
        logging.info(f'Trying to match url: {result} "')
        p2 = re.compile("^http.*")
        return p2.search(result)


def emptish(string: Union[str, None]) -> bool:
    result = remove_special_chars(string)
    return len(result) == 0


def ends_in_new_line(string) -> bool:
    return string.endswith("\n")


def remove_new_line_end(string) -> str:
    return string.rstrip("\n")


class StringManipulation:
    """
    @ToDo: break it down to functions  class is for state or higher order functions, here does not make sense to use a
    @deprecated use the functions instead, theres no domain specific groupping here
    """

    @staticmethod
    def tokenize(text):
        text_vec = text.split()
        return list(map(StringManipulation.chomp, text_vec))

    @staticmethod
    def chomp(x):
        if x.endswith("\r\n"):
            return x[:-2]
        if x.endswith("\n") or x.endswith("\r"):
            return x[:-1]
        return x

    @staticmethod
    def clean_sentence(x):
        result = StringManipulation.chomp(x)
        result = result.strip()

        return result
