# try not to load modules with dependencies here otherwise everything has to be installed
# LEARNING:
# expose modules without their path that can change when they are very popular
# rather than from grimoire.logger import Logger do
# from grimoire import Logger even if logger is inside grimoire.logger.Logger
# logger.Logger is just not pythonic and adds a lot of verbosity

import functools
import json
import os
import sys
from datetime import timedelta
from typing import List

## Time functions
# Go to time.py
import yaml

# namespace exposure imports
import grimoire.debug
from grimoire.core.logger import Logger
from grimoire.shell import shell as s


def file_exists(name):
    """
    @deprecated use file.* functions instead
    the correct command is:
    os.path.exists(name)
    """
    return os.path.exists(name)


def reduce(f, array, initial_val=0):
    return functools.reduce(f, array, initial_val)


def get_stdin():
    return sys.stdin.read()


def json_content(filename):
    import json

    with open(filename) as f:
        data = json.load(f)

    return data


# keep here the public API
def yml_content(filename):
    with open(filename) as f:
        data = yaml.load(f, yaml.FullLoader)

    return data


def file_content(file_name) -> List[str]:
    """
    @deprecated use file.* functions instead
    """
    f = open(file_name)
    return f.readlines()


def yml2json(file):
    content = yml_content(file)
    printj(content)


def tmp_filename() -> str:
    """
    @deprecated use file.* functions instead
    """
    import uuid

    return "/tmp/" + str(uuid.uuid4())[:20].replace("-", "")


def jsonb(data):
    """ Makes a json beautiful """
    return json.dumps(data, indent=4)


def printj(data):
    print(jsonb)


def write_file(file, data):
    """
    @deprecated use file.* functions instead
    """
    with open(file, "w+") as f:
        f.write(data)


def append_file(file, data):
    with open(file, "a+") as f:
        f.write(data)


def import_from_path(path, modulename):
    """
    use it like:
    foo = g.import_from_path('/tmp/foo.py', 'foo')
    """
    import importlib.util

    spec = importlib.util.spec_from_file_location(modulename, path)
    foo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(foo)
    return foo


def notify_send(msg):
    os.system(f'notify-send "{msg}"')


def write_variable_to_py_file(varname, varvalue, file):
    """
    saves a variable in a parseable python file
    useful for caching the load of heavy yaml files
    """
    import pprint

    string = f"{pprint.pformat(varvalue)}"
    write_file(file, f"{varname} = {string}")


def hello():
    print("Hello grimoire user!")


def get_script_path():
    """
    returns the location where the script that imports this function is being runned from
    """
    return os.path.dirname(os.path.realpath(sys.argv[0]))


script_path = get_script_path


def partition_range(lst, n):
    return [lst[i::n] for i in range(n)]


def get_index(a_list, index, default_value=None):
    try:
        return a_list[index]
    except:
        return default_value


def seconds_to_str(seconds: int):
    """ Returns a human readable string representing the amount of time"""
    return str(timedelta(seconds=seconds))


def system_info():
    return {"cpu_count": os.cpu_count()}
