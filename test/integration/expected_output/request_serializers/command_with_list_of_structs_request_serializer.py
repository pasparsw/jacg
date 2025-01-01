from logging import getLogger

from structs.command_with_list_of_structs_request import CommandWithListOfStructsRequest

LOGGER = getLogger("CommandWithListOfStructsRequestSerializer")


class CommandWithListOfStructsRequestSerializer:
    @staticmethod
    def serialize(request: CommandWithListOfStructsRequest) -> dict:
        LOGGER.debug(f"Serializing commandWithListOfStructs request to dictionary")

        return {
            'arg': [{
                'field_1': element.field_1,
                'field_2': element.field_2,
            } for element in request.arg],
        }
