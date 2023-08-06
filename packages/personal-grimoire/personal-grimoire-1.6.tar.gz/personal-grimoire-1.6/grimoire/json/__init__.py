import json
import logging
from pprint import pformat

from pygments import highlight
from pygments.formatters import TerminalTrueColorFormatter
from pygments.lexers import PythonLexer


def print_pretty(obj):
    if type(obj) is str:
        obj = json.loads(obj)
        logging.info("Converting object to json parsed")
    print(highlight(pformat(obj), PythonLexer(), TerminalTrueColorFormatter()))
