import unittest

from unittest.mock import MagicMock, Mock, patch, call

from src.api_model.command_model import CommandModel
from src.api_model.struct_model import StructModel
from src.generators.generator_interface import GeneratedContent
from src.generators.request_serializers_generator import RequestSerializersGenerator, \
    REQUEST_SERIALIZER_TEMPLATE_FILE_PATH


@patch("src.generators.request_serializers_generator.load_file_content")
class TestRequestSerializersGenerator(unittest.TestCase):
    def test_generate(self, load_file_content_mock):
        some_struct: StructModel = StructModel(
            name="SomeStruct",
            fields=[]
        )
        some_other_struct: StructModel = StructModel(
            name="SomeOtherStruct",
            fields=[]
        )
        some_command: CommandModel = CommandModel(name="SomeCommand", request=some_struct, response=some_other_struct,
                                                  silent=False)
        some_other_command: CommandModel = CommandModel(name="SomeOtherCommand", request=some_other_struct,
                                                        response=some_struct, silent=False)
        api_model = MagicMock(
            enums={},
            structs={
                "SomeStruct": some_struct,
                "SomeOtherStruct": some_other_struct,
            },
            commands=[some_command, some_other_command]
        )
        template: str = "request_serializer_template"
        some_request_serializer_definition: str = "request_serializer_1"
        some_other_request_serializer_definition: str = "request_serializer_1"
        expected_output: GeneratedContent = {
            "request_serializers/some_command_request_serializer.py": some_request_serializer_definition,
            "request_serializers/some_other_command_request_serializer.py": some_other_request_serializer_definition
        }

        empy_interpreter = MagicMock(expand=Mock())

        load_file_content_mock.return_value = template
        empy_interpreter.expand.side_effect = [
            some_request_serializer_definition,
            some_other_request_serializer_definition
        ]

        output: GeneratedContent = RequestSerializersGenerator().generate(empy_interpreter, api_model)

        load_file_content_mock.assert_called_once_with(REQUEST_SERIALIZER_TEMPLATE_FILE_PATH)
        empy_interpreter.expand.assert_has_calls([
            call(template, {"model": some_command, "struct_models": api_model.structs, "enum_models": api_model.enums}),
            call(template, {"model": some_other_command, "struct_models": api_model.structs, "enum_models": api_model.enums}),
        ])

        self.assertDictEqual(output, expected_output)
