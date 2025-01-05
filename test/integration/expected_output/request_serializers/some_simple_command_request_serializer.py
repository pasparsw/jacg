from logging import getLogger

from ..structs.some_simple_command_request import SomeSimpleCommandRequest

LOGGER = getLogger("SomeSimpleCommandRequestSerializer")


class SomeSimpleCommandRequestSerializer:
    @staticmethod
    def serialize(request: SomeSimpleCommandRequest) -> dict:
        LOGGER.debug(f"Serializing someSimpleCommand request to dictionary")

        return {
            'arg': request.arg,
        }
