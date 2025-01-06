from example.output.api_client.my_api_client import MyApiClient
from example.output.api_connectors.api_connector_factory import ApiConnectorFactory, ApiConnectorType

from example.output.structs.some_simple_command_request import SomeSimpleCommandRequest
from example.output.structs.some_simple_command_response import SomeSimpleCommandResponse

from example.output.structs.command_with_default_arg_request import CommandWithDefaultArgRequest
from example.output.structs.command_with_default_arg_response import CommandWithDefaultArgResponse

from example.output.structs.command_with_enums_request import CommandWithEnumsRequest, MyEnum
from example.output.structs.command_with_enums_response import CommandWithEnumsResponse

from example.output.structs.command_with_struct_arg_request import CommandWithStructArgRequest, MyStruct
from example.output.structs.command_with_struct_arg_response import CommandWithStructArgResponse

from example.output.structs.command_with_lists_request import CommandWithListsRequest
from example.output.structs.command_with_lists_response import CommandWithListsResponse

from example.output.structs.command_with_list_of_structs_request import CommandWithListOfStructsRequest
from example.output.structs.command_with_list_of_structs_response import CommandWithListOfStructsResponse

from example.output.structs.command_with_nested_structs_request import CommandWithNestedStructsRequest
from example.output.structs.command_with_nested_structs_response import CommandWithNestedStructsResponse, MyComplexStruct


def custom_response_validation_callback(response_data: dict) -> None:
    print(f"Validating response: {response_data}")


if __name__ == "__main__":
    api_connector = ApiConnectorFactory.create(ApiConnectorType.SSL)
    api_client = MyApiClient(api_connector)

    api_client.set_response_validation_cb(custom_response_validation_callback)
    api_client.connect()

    # someSimpleCommand
    request = SomeSimpleCommandRequest(
        arg=12
    )
    response: SomeSimpleCommandResponse = api_client.some_simple_command(request)
    print(f"Returned value: {response.returned_value}")

    # commandWithDefaultArg
    request = CommandWithDefaultArgRequest(
        arg_2=3.14
    )
    response: CommandWithDefaultArgResponse = api_client.command_with_default_arg(request)
    print(f"Returned value: {response.returned_value}")

    # commandWithEnums
    request = CommandWithEnumsRequest(
        arg=MyEnum.VALUE_2
    )
    response: CommandWithEnumsResponse = api_client.command_with_enums(request)
    print(f"Returned value: {response.returned_value}")

    # commandWithStructArgs
    request = CommandWithStructArgRequest(
        arg=MyStruct(
            field_1='value',
            field_2=12
        )
    )
    response: CommandWithStructArgResponse = api_client.command_with_struct_arg(request)
    print(f"Returned valued: "
          f"field_3 = {response.returned_value.field_3},"
          f"field_4 = {response.returned_value.field_4}")

    # commandWithLists
    request = CommandWithListsRequest(
        arg=['ab', 'cd', 'ef']
    )
    response: CommandWithListsResponse = api_client.command_with_lists(request)
    print(f"Returned value:")
    for element in response.returned_value:
        print(element)

    # commandWithListOfStructs
    request = CommandWithListOfStructsRequest(
        arg=[
            MyStruct(field_1='value_1', field_2=12),
            MyStruct(field_1='value_2', field_2=24),
        ]
    )
    response: CommandWithListOfStructsResponse = api_client.command_with_list_of_structs(request)
    print(f"Returned value:")
    for element in response.returned_value:
        print(f"field_1 = {element.field_3}")
        print(f"field_2 = {element.field_4}")

    # commandWithNestedStructs
    request = CommandWithNestedStructsRequest(
        arg=12
    )
    response: CommandWithNestedStructsResponse = api_client.command_with_nested_structs(request)
    print(f"Returned value:")
    print(f"field_5 = ")
    print(f"  field_1 = {response.returned_value.field_5.field_1}")
    print(f"  field_2 = {response.returned_value.field_5.field_2}")
    print(f"field_6 = ")
    for element in response.returned_value.field_6:
        print(f"  field_3 = {element.field_3}")
        print(f"  field_4 = {element.field_4}")
