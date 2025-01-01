from logging import getLogger

from structs.command_with_lists_response import CommandWithListsResponse



LOGGER = getLogger("CommandWithListsResponseDeserializer")


class CommandWithListsResponseDeserializer:
    @staticmethod
    def deserialize(response: CommandWithListsResponse) -> dict:
        LOGGER.debug(f"Deserializing commandWithLists response from dictionary")

        return CommandWithListsResponse(
            returned_value=response['returned_value'],
        )
