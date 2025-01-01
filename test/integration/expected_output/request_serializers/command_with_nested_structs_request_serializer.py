from logging import getLogger

from structs.command_with_nested_structs_request import CommandWithNestedStructsRequest

LOGGER = getLogger("CommandWithNestedStructsRequestSerializer")


class CommandWithNestedStructsRequestSerializer:
    @staticmethod
    def serialize(request: CommandWithNestedStructsRequest) -> dict:
        LOGGER.debug(f"Serializing commandWithNestedStructs request to dictionary")

        return {
            'arg': request.arg,
        }
