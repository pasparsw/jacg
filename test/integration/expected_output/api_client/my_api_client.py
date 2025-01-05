from logging import getLogger
from typing import Callable

from ..api_connectors.connectors.api_connector_interface import ApiConnectorInterface

from ..structs.some_simple_command_request import SomeSimpleCommandRequest
from ..structs.some_simple_command_response import SomeSimpleCommandResponse
from ..structs.command_with_default_arg_request import CommandWithDefaultArgRequest
from ..structs.command_with_default_arg_response import CommandWithDefaultArgResponse
from ..structs.command_with_enums_request import CommandWithEnumsRequest
from ..structs.command_with_enums_response import CommandWithEnumsResponse
from ..structs.command_with_struct_arg_request import CommandWithStructArgRequest
from ..structs.command_with_struct_arg_response import CommandWithStructArgResponse
from ..structs.command_with_lists_request import CommandWithListsRequest
from ..structs.command_with_lists_response import CommandWithListsResponse
from ..structs.command_with_list_of_structs_request import CommandWithListOfStructsRequest
from ..structs.command_with_list_of_structs_response import CommandWithListOfStructsResponse
from ..structs.command_with_nested_structs_request import CommandWithNestedStructsRequest
from ..structs.command_with_nested_structs_response import CommandWithNestedStructsResponse

# request serializers
from ..request_serializers.some_simple_command_request_serializer import SomeSimpleCommandRequestSerializer
from ..request_serializers.command_with_default_arg_request_serializer import CommandWithDefaultArgRequestSerializer
from ..request_serializers.command_with_enums_request_serializer import CommandWithEnumsRequestSerializer
from ..request_serializers.command_with_struct_arg_request_serializer import CommandWithStructArgRequestSerializer
from ..request_serializers.command_with_lists_request_serializer import CommandWithListsRequestSerializer
from ..request_serializers.command_with_list_of_structs_request_serializer import CommandWithListOfStructsRequestSerializer
from ..request_serializers.command_with_nested_structs_request_serializer import CommandWithNestedStructsRequestSerializer

# response deserializers
from ..response_deserializers.some_simple_command_response_deserializer import SomeSimpleCommandResponseDeserializer
from ..response_deserializers.command_with_default_arg_response_deserializer import CommandWithDefaultArgResponseDeserializer
from ..response_deserializers.command_with_enums_response_deserializer import CommandWithEnumsResponseDeserializer
from ..response_deserializers.command_with_struct_arg_response_deserializer import CommandWithStructArgResponseDeserializer
from ..response_deserializers.command_with_lists_response_deserializer import CommandWithListsResponseDeserializer
from ..response_deserializers.command_with_list_of_structs_response_deserializer import CommandWithListOfStructsResponseDeserializer
from ..response_deserializers.command_with_nested_structs_response_deserializer import CommandWithNestedStructsResponseDeserializer


LOGGER = getLogger("MyApiClient")

def log_debug(message: str, is_silent: bool) -> None:
    if is_silent:
        return
    LOGGER.debug(message)


class InvalidRequestType(Exception):
    pass


class MyApiClient:
    def __init__(self, api_connector: ApiConnectorInterface):
        self.__api_connector: ApiConnectorInterface = api_connector
        self.__validate_response = None

    def connect(self) -> None:
        self.__api_connector.connect(hostname="some.hostname.com",
                                     port=1234,
                                     response_buffer_size=1024,
                                     response_timeout=5,
                                     socket_timeout=3)

    def set_response_validation_cb(self, response_validation_cb: Callable[[dict], None]) -> None:
        self.__validate_response: Callable[[dict], None] = response_validation_cb

    def some_simple_command(self, request: SomeSimpleCommandRequest) -> SomeSimpleCommandResponse:
        if not isinstance(request, SomeSimpleCommandRequest):
            raise InvalidRequestType(f"Command some_simple_command requires request of type SomeSimpleCommandRequest, but the request of type "
                                     f"{type(request)} has been provided!")

        log_debug(f"Serializing request: {request}", is_silent=False)
        serialized_request: dict = SomeSimpleCommandRequestSerializer.serialize(request)

        log_debug(f"Sending request {serialized_request}", is_silent=False)
        serialized_response: dict = self.__api_connector.send(serialized_request)

        log_debug(f"Received response: {serialized_response}", is_silent=False)
        self.__call_response_validation_cb(serialized_response)

        deserialized_response: SomeSimpleCommandResponse = SomeSimpleCommandResponseDeserializer.deserialize(serialized_response)
        log_debug(f"Deserialized response: {deserialized_response}", is_silent=False)

        return deserialized_response

    def command_with_default_arg(self, request: CommandWithDefaultArgRequest) -> CommandWithDefaultArgResponse:
        if not isinstance(request, CommandWithDefaultArgRequest):
            raise InvalidRequestType(f"Command command_with_default_arg requires request of type CommandWithDefaultArgRequest, but the request of type "
                                     f"{type(request)} has been provided!")

        log_debug(f"Serializing request: {request}", is_silent=False)
        serialized_request: dict = CommandWithDefaultArgRequestSerializer.serialize(request)

        log_debug(f"Sending request {serialized_request}", is_silent=False)
        serialized_response: dict = self.__api_connector.send(serialized_request)

        log_debug(f"Received response: {serialized_response}", is_silent=False)
        self.__call_response_validation_cb(serialized_response)

        deserialized_response: CommandWithDefaultArgResponse = CommandWithDefaultArgResponseDeserializer.deserialize(serialized_response)
        log_debug(f"Deserialized response: {deserialized_response}", is_silent=False)

        return deserialized_response

    def command_with_enums(self, request: CommandWithEnumsRequest) -> CommandWithEnumsResponse:
        if not isinstance(request, CommandWithEnumsRequest):
            raise InvalidRequestType(f"Command command_with_enums requires request of type CommandWithEnumsRequest, but the request of type "
                                     f"{type(request)} has been provided!")

        log_debug(f"Serializing request: {request}", is_silent=False)
        serialized_request: dict = CommandWithEnumsRequestSerializer.serialize(request)

        log_debug(f"Sending request {serialized_request}", is_silent=False)
        serialized_response: dict = self.__api_connector.send(serialized_request)

        log_debug(f"Received response: {serialized_response}", is_silent=False)
        self.__call_response_validation_cb(serialized_response)

        deserialized_response: CommandWithEnumsResponse = CommandWithEnumsResponseDeserializer.deserialize(serialized_response)
        log_debug(f"Deserialized response: {deserialized_response}", is_silent=False)

        return deserialized_response

    def command_with_struct_arg(self, request: CommandWithStructArgRequest) -> CommandWithStructArgResponse:
        if not isinstance(request, CommandWithStructArgRequest):
            raise InvalidRequestType(f"Command command_with_struct_arg requires request of type CommandWithStructArgRequest, but the request of type "
                                     f"{type(request)} has been provided!")

        log_debug(f"Serializing request: {request}", is_silent=False)
        serialized_request: dict = CommandWithStructArgRequestSerializer.serialize(request)

        log_debug(f"Sending request {serialized_request}", is_silent=False)
        serialized_response: dict = self.__api_connector.send(serialized_request)

        log_debug(f"Received response: {serialized_response}", is_silent=False)
        self.__call_response_validation_cb(serialized_response)

        deserialized_response: CommandWithStructArgResponse = CommandWithStructArgResponseDeserializer.deserialize(serialized_response)
        log_debug(f"Deserialized response: {deserialized_response}", is_silent=False)

        return deserialized_response

    def command_with_lists(self, request: CommandWithListsRequest) -> CommandWithListsResponse:
        if not isinstance(request, CommandWithListsRequest):
            raise InvalidRequestType(f"Command command_with_lists requires request of type CommandWithListsRequest, but the request of type "
                                     f"{type(request)} has been provided!")

        log_debug(f"Serializing request: {request}", is_silent=False)
        serialized_request: dict = CommandWithListsRequestSerializer.serialize(request)

        log_debug(f"Sending request {serialized_request}", is_silent=False)
        serialized_response: dict = self.__api_connector.send(serialized_request)

        log_debug(f"Received response: {serialized_response}", is_silent=False)
        self.__call_response_validation_cb(serialized_response)

        deserialized_response: CommandWithListsResponse = CommandWithListsResponseDeserializer.deserialize(serialized_response)
        log_debug(f"Deserialized response: {deserialized_response}", is_silent=False)

        return deserialized_response

    def command_with_list_of_structs(self, request: CommandWithListOfStructsRequest) -> CommandWithListOfStructsResponse:
        if not isinstance(request, CommandWithListOfStructsRequest):
            raise InvalidRequestType(f"Command command_with_list_of_structs requires request of type CommandWithListOfStructsRequest, but the request of type "
                                     f"{type(request)} has been provided!")

        log_debug(f"Serializing request: {request}", is_silent=False)
        serialized_request: dict = CommandWithListOfStructsRequestSerializer.serialize(request)

        log_debug(f"Sending request {serialized_request}", is_silent=False)
        serialized_response: dict = self.__api_connector.send(serialized_request)

        log_debug(f"Received response: {serialized_response}", is_silent=False)
        self.__call_response_validation_cb(serialized_response)

        deserialized_response: CommandWithListOfStructsResponse = CommandWithListOfStructsResponseDeserializer.deserialize(serialized_response)
        log_debug(f"Deserialized response: {deserialized_response}", is_silent=False)

        return deserialized_response

    def command_with_nested_structs(self, request: CommandWithNestedStructsRequest) -> CommandWithNestedStructsResponse:
        if not isinstance(request, CommandWithNestedStructsRequest):
            raise InvalidRequestType(f"Command command_with_nested_structs requires request of type CommandWithNestedStructsRequest, but the request of type "
                                     f"{type(request)} has been provided!")

        log_debug(f"Serializing request: {request}", is_silent=False)
        serialized_request: dict = CommandWithNestedStructsRequestSerializer.serialize(request)

        log_debug(f"Sending request {serialized_request}", is_silent=False)
        serialized_response: dict = self.__api_connector.send(serialized_request)

        log_debug(f"Received response: {serialized_response}", is_silent=False)
        self.__call_response_validation_cb(serialized_response)

        deserialized_response: CommandWithNestedStructsResponse = CommandWithNestedStructsResponseDeserializer.deserialize(serialized_response)
        log_debug(f"Deserialized response: {deserialized_response}", is_silent=False)

        return deserialized_response


    def __call_response_validation_cb(self, serialized_response: dict) -> None:
        if self.__validate_response:
            self.__validate_response(serialized_response)
