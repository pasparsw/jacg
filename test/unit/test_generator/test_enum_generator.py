import unittest

from unittest.mock import MagicMock, Mock, patch, call

from src.api_model.enum_field_model import EnumFieldModel
from src.api_model.enum_model import EnumModel
from src.generators.enums_generator import EnumsGenerator, ENUM_TEMPLATE_FILE_PATH
from src.generators.generator_interface import GeneratedContent


@patch("src.generators.enums_generator.load_file_content")
class TestEnumGenerator(unittest.TestCase):
    def test_generate(self, load_file_content_mock):
        enum_model_1: EnumModel = EnumModel(
            name="SomeEnum",
            fields=[
                EnumFieldModel(name="SomeField1", value="1"),
                EnumFieldModel(name="SomeField2", value="2"),
                EnumFieldModel(name="SomeField3", value="3"),
            ]
        )
        enum_model_2: EnumModel = EnumModel(
            name="AnotherEnum",
            fields=[
                EnumFieldModel(name="SomeOtherField1", value="4"),
                EnumFieldModel(name="SomeOtherField2", value="5"),
                EnumFieldModel(name="SomeOtherField3", value="6"),
            ]
        )
        api_model = MagicMock(
            enums={
                "SomeEnum": enum_model_1,
                "AnotherEnum": enum_model_2
            }
        )
        template: str = "enum_template"
        some_enum_definition: str = "enum_1"
        another_enum_definition: str = "enum_2"
        expected_output: GeneratedContent = {
            "enums/some_enum.py": some_enum_definition,
            "enums/another_enum.py": another_enum_definition
        }

        empy_interpreter = MagicMock(expand=Mock())

        load_file_content_mock.return_value = template
        empy_interpreter.expand.side_effect = [
            some_enum_definition,
            another_enum_definition
        ]

        output: GeneratedContent = EnumsGenerator().generate(empy_interpreter, api_model)

        load_file_content_mock.assert_called_once_with(ENUM_TEMPLATE_FILE_PATH)
        empy_interpreter.expand.assert_has_calls([
            call(template, {"model": enum_model_1}),
            call(template, {"model": enum_model_2}),
        ])

        for path, content in expected_output.items():
            self.assertTrue(path in output)
            self.assertEqual(output[path], expected_output[path])
