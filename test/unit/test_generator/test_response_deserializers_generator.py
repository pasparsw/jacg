import unittest

from unittest.mock import MagicMock, Mock, patch, call

from src.api_model.command_model import CommandModel
from src.api_model.struct_model import StructModel
from src.generators.generator_interface import GeneratedContent
from src.generators.response_deserializers_generator import ResponseDeserializersGenerator, \
    RESPONSE_DESERIALIZER_TEMPLATE_FILE_PATH


@patch("src.generators.response_deserializers_generator.load_file_content")
class TestResponseDeserializersGenerator(unittest.TestCase):
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
        template: str = "response_deserializer_template"
        some_response_deserializer_definition: str = "response_deserializer_1"
        some_other_response_deserializer_definition: str = "response_deserializer_1"
        expected_output: GeneratedContent = {
            "response_deserializers/some_command_response_deserializer.py": some_response_deserializer_definition,
            "response_deserializers/some_other_command_response_deserializer.py": some_other_response_deserializer_definition
        }

        empy_interpreter = MagicMock(expand=Mock())

        load_file_content_mock.return_value = template
        empy_interpreter.expand.side_effect = [
            some_response_deserializer_definition,
            some_other_response_deserializer_definition
        ]

        output: GeneratedContent = ResponseDeserializersGenerator().generate(empy_interpreter, api_model)

        load_file_content_mock.assert_called_once_with(RESPONSE_DESERIALIZER_TEMPLATE_FILE_PATH)
        empy_interpreter.expand.assert_has_calls([
            call(template, {"model": some_command, "struct_models": api_model.structs, "enum_models": api_model.enums}),
            call(template, {"model": some_other_command, "struct_models": api_model.structs, "enum_models": api_model.enums}),
        ])

        self.assertDictEqual(output, expected_output)
