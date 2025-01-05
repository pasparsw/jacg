from logging import getLogger

from ..structs.some_simple_command_response import SomeSimpleCommandResponse



LOGGER = getLogger("SomeSimpleCommandResponseDeserializer")


class SomeSimpleCommandResponseDeserializer:
    @staticmethod
    def deserialize(response: dict) -> SomeSimpleCommandResponse:
        LOGGER.debug(f"Deserializing someSimpleCommand response from dictionary")

        return SomeSimpleCommandResponse(
            returned_value=response['returned_value'],
        )
