from logging import getLogger

from ..structs.command_with_struct_arg_response import CommandWithStructArgResponse

from ..structs.my_other_struct import MyOtherStruct


LOGGER = getLogger("CommandWithStructArgResponseDeserializer")


class CommandWithStructArgResponseDeserializer:
    @staticmethod
    def deserialize(response: dict) -> CommandWithStructArgResponse:
        LOGGER.debug(f"Deserializing commandWithStructArg response from dictionary")

        return CommandWithStructArgResponse(
            returned_value=MyOtherStruct(
                field_3=response['returned_value']['field_3'],
                field_4=response['returned_value']['field_4'],
            ),
        )
