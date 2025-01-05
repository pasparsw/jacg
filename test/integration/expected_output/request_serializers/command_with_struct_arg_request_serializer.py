from logging import getLogger

from ..structs.command_with_struct_arg_request import CommandWithStructArgRequest

LOGGER = getLogger("CommandWithStructArgRequestSerializer")


class CommandWithStructArgRequestSerializer:
    @staticmethod
    def serialize(request: CommandWithStructArgRequest) -> dict:
        LOGGER.debug(f"Serializing commandWithStructArg request to dictionary")

        return {
            'arg': {
                'field_1': request.arg.field_1,
                'field_2': request.arg.field_2,
            },
        }
