import os

from pydantic import BaseSettings

dir_path = os.path.dirname(os.path.realpath(__file__))
# @TODO remove the / from this variable
GRIMOIRE_PROJECT_ROOT = f"{dir_path}/../"

LOG_FILE = "/data/grimoire/logs/latest"


class Configuration(BaseSettings):
    # default is production ready
    API_PORT = 5007
    LOG_FILE = LOG_FILE
    # where json formatted logs go
    LOG_FILE_JSON = "/data/grimoire/logs/latest.json"
    # using a different than the default 6379 to not conflict with docker
    REDIS_PORT = "6378"
    REDIS_HOST = "localhost"


config = Configuration()
