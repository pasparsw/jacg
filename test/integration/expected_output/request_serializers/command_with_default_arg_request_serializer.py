from logging import getLogger

from structs.command_with_default_arg_request import CommandWithDefaultArgRequest

LOGGER = getLogger("CommandWithDefaultArgRequestSerializer")


class CommandWithDefaultArgRequestSerializer:
    @staticmethod
    def serialize(request: CommandWithDefaultArgRequest) -> dict:
        LOGGER.debug(f"Serializing commandWithDefaultArg request to dictionary")

        return {
            'arg_2': request.arg_2,
            'arg_1': request.arg_1,
            'arg_3': request.arg_3,
        }
