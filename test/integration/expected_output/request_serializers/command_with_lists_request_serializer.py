from logging import getLogger

from ..structs.command_with_lists_request import CommandWithListsRequest

LOGGER = getLogger("CommandWithListsRequestSerializer")


class CommandWithListsRequestSerializer:
    @staticmethod
    def serialize(request: CommandWithListsRequest) -> dict:
        LOGGER.debug(f"Serializing commandWithLists request to dictionary")

        return {
            'arg': request.arg,
        }
