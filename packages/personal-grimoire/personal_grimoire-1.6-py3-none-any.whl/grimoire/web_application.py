import os

from flask import Flask, jsonify, make_response, request
from flask_cors import CORS

from grimoire.config import LOG_FILE
from grimoire.error_handler import ErrorHandler
from grimoire.git import get_commit_hash
from grimoire.observability.metrics import Metrics
from grimoire.search_run.search_and_run import SearchAndRunCli
from grimoire.shell import shell
from grimoire.smartimmersion.application.ImmerseText import ImmerseText
from grimoire.smartimmersion.smartimmersion import SmartImmersion
from grimoire.startup import ApplicationStartup

app = Flask(__name__)
CORS(app)
ApplicationStartup().log_to_file(LOG_FILE).initialize()


@app.route("/search_run/dmenu")
def searchrun():
    Metrics.time_function(SearchAndRunCli().dmenu, "search_dmenu_time_to_execute")
    return "Ok"


@app.route("/translate")
def immerse():
    """keep this endpoint dumb simple, concentrating the complexity on the smart immersion module"""
    query = request.args.get("q")
    return ImmerseText().immerse_web(query, request)


@app.route("/translate_back")
def translate_back():
    """keep this endpoint dumb simple, concentrating the complexity on the smart immersion module"""
    query = request.args.get("q")
    return SmartImmersion().register_hard(query)


@app.route("/_info")
def info():

    return {
        "cpu_num": os.cpu_count(),
        "uptime": shell.run_with_result("uptime || cat /proc/uptime"),
        "commit": get_commit_hash(),
    }


@app.route("/_fail")
def simulate_error():
    raise Exception("Simulated error")


@app.errorhandler(Exception)
def web_error_handler(exception):
    ErrorHandler().handle(exception)
    error = ErrorHandler.exception_to_entity(exception)
    response = make_response(jsonify(error.serialize()), error.http_status)

    response.headers["Content-Type"] = "application/problem+json"
    return response


@app.errorhandler(404)
def page_not_found(exception):
    error = ErrorHandler.exception_to_entity(exception)
    response = make_response(jsonify(error.serialize()), error.http_status)
    response.headers["Content-Type"] = "application/problem+json"
    return response


@app.route("/")
def main():
    return f"Grimoire API v1.02"
