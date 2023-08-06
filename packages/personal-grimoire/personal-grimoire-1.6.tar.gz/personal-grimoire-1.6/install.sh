#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"


set -e
pip install -r requirements_dev.txt
pip install -e "$DIR"
pip install pre-commit
pre-commit install
