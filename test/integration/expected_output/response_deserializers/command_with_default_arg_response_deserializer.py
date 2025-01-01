from logging import getLogger

from structs.command_with_default_arg_response import CommandWithDefaultArgResponse



LOGGER = getLogger("CommandWithDefaultArgResponseDeserializer")


class CommandWithDefaultArgResponseDeserializer:
    @staticmethod
    def deserialize(response: CommandWithDefaultArgResponse) -> dict:
        LOGGER.debug(f"Deserializing commandWithDefaultArg response from dictionary")

        return CommandWithDefaultArgResponse(
            returned_value=response['returned_value'],
        )
