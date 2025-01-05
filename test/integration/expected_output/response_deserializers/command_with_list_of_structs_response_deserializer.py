from logging import getLogger

from ..structs.command_with_list_of_structs_response import CommandWithListOfStructsResponse

from ..structs.my_other_struct import MyOtherStruct


LOGGER = getLogger("CommandWithListOfStructsResponseDeserializer")


class CommandWithListOfStructsResponseDeserializer:
    @staticmethod
    def deserialize(response: dict) -> CommandWithListOfStructsResponse:
        LOGGER.debug(f"Deserializing commandWithListOfStructs response from dictionary")

        return CommandWithListOfStructsResponse(
            returned_value=[MyOtherStruct(
                field_3=element['field_3'],
                field_4=element['field_4'],
            ) for element in response['returned_value']],
        )
