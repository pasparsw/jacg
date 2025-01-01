from logging import getLogger

from structs.command_with_nested_structs_response import CommandWithNestedStructsResponse

from structs.my_struct import MyStruct
from structs.my_other_struct import MyOtherStruct
from structs.my_complex_struct import MyComplexStruct


LOGGER = getLogger("CommandWithNestedStructsResponseDeserializer")


class CommandWithNestedStructsResponseDeserializer:
    @staticmethod
    def deserialize(response: CommandWithNestedStructsResponse) -> dict:
        LOGGER.debug(f"Deserializing commandWithNestedStructs response from dictionary")

        return CommandWithNestedStructsResponse(
            returned_value=MyComplexStruct(
                field_5=MyStruct(
                    field_1=response['returned_value']['field_5']['field_1'],
                    field_2=response['returned_value']['field_5']['field_2'],
                ),
                field_6=[MyOtherStruct(
                    field_3=element['field_3'],
                    field_4=element['field_4'],
                ) for element in response['returned_value']['field_6']],
            ),
        )
