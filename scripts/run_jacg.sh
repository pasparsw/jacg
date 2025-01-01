#!/bin/bash

set -e

SCRIPTS_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
REPO_DIR="$SCRIPTS_DIR/.."
INTERPRETER_PATH="$REPO_DIR/venv/bin/python3"
MAIN_PATH="$REPO_DIR/src/main.py"

$INTERPRETER_PATH $MAIN_PATH $@
