import sys
import os

from src.paths import REPO_PATH

sys.path.append(os.path.join(REPO_PATH, "example", "output"))

from output.api_client.my_api_client import MyApiClient

from output.structs.some_simple_command_request import SomeSimpleCommandRequest
from output.structs.some_simple_command_response import SomeSimpleCommandResponse

from output.structs.command_with_default_arg_request import CommandWithDefaultArgRequest
from output.structs.command_with_default_arg_response import CommandWithDefaultArgResponse

from output.structs.command_with_enums_request import CommandWithEnumsRequest, MyEnum
from output.structs.command_with_enums_response import CommandWithEnumsResponse

from output.structs.command_with_struct_arg_request import CommandWithStructArgRequest, MyStruct
from output.structs.command_with_struct_arg_response import CommandWithStructArgResponse

from output.structs.command_with_lists_request import CommandWithListsRequest
from output.structs.command_with_lists_response import CommandWithListsResponse

from output.structs.command_with_list_of_structs_request import CommandWithListOfStructsRequest
from output.structs.command_with_list_of_structs_response import CommandWithListOfStructsResponse

from output.structs.command_with_nested_structs_request import CommandWithNestedStructsRequest
from output.structs.command_with_nested_structs_response import CommandWithNestedStructsResponse, MyComplexStruct



if __name__ == "__main__":
    api_client = MyApiClient()
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
        print(f"field_1 = {element.field_1}")
        print(f"field_2 = {element.field_2}")

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
