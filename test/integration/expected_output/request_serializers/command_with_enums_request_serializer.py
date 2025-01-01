from logging import getLogger

from structs.command_with_enums_request import CommandWithEnumsRequest

LOGGER = getLogger("CommandWithEnumsRequestSerializer")


class CommandWithEnumsRequestSerializer:
    @staticmethod
    def serialize(request: CommandWithEnumsRequest) -> dict:
        LOGGER.debug(f"Serializing commandWithEnums request to dictionary")

        return {
            'arg': request.arg,
        }
