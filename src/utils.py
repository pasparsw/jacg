import json

from logging import getLogger
from typing import List

LOGGER = getLogger("Utils")

def load_json(path: str) -> dict:
    LOGGER.debug(f"Loading JSON from {path}")

    with open(path) as file:
        return json.load(file)


def load_file_content(path: str):
    LOGGER.debug(f"Loading file from {path}")

    with open(path) as file:
        return file.read()


def save_to_file(path: str, content: str):
    LOGGER.debug(f"Saving to file {path}")

    with open(path, 'w') as file:
        file.write(content)


def capitalize(input: str) -> str:
    return input[0].upper() + input[1:]


def camel_case_to_snake_case(camel_case: str) -> str:
    snake_case = ''
    for i, c in enumerate(camel_case):
        if i > 0 and c.isupper():
            snake_case += '_'
        snake_case += c.lower()

    return snake_case.replace('__', '_')


def snake_case_to_camel_case(input_string: str) -> str:
    elements: List[str] = input_string.split("_")
    output: str = ""

    for element in elements:
        output += capitalize(element)

    return output
