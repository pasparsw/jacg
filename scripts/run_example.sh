#!/bin/bash

set -e

SCRIPTS_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
REPO_DIR="$SCRIPTS_DIR/.."
INTERPRETER_PATH="$REPO_DIR/venv/bin/python3"
MAIN_PATH="$REPO_DIR/src/main.py"
EXAMPLE_SPEC_FILE_PATH="$REPO_DIR/example/example_api_spec.json"
EXAMPLE_OUTPUT_DIR="$REPO_DIR/example/output"

$INTERPRETER_PATH $MAIN_PATH run -spec $EXAMPLE_SPEC_FILE_PATH -output $EXAMPLE_OUTPUT_DIR $@
