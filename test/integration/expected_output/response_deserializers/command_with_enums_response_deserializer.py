from logging import getLogger

from ..structs.command_with_enums_response import CommandWithEnumsResponse

from ..enums.my_other_enum import MyOtherEnum


LOGGER = getLogger("CommandWithEnumsResponseDeserializer")


class CommandWithEnumsResponseDeserializer:
    @staticmethod
    def deserialize(response: dict) -> CommandWithEnumsResponse:
        LOGGER.debug(f"Deserializing commandWithEnums response from dictionary")

        return CommandWithEnumsResponse(
            returned_value=[MyOtherEnum(value) for value in response['returned_value']],
        )
