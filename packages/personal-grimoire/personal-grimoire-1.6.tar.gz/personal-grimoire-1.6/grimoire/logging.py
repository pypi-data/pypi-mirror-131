import json

from grimoire.config import config

import logging

def serialize(record):
    subset = {"timestamp": record["time"].timestamp()}
    return subset


def formatter(record):
    # Note this function returns the string to be formatted, not the actual message to be logged
    record["extra"]["serialized"] = serialize(record)
    return "{extra[serialized]}\n"


