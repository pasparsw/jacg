import unittest

from unittest.mock import MagicMock, Mock, call, patch

from src.api_model.struct_field_model import StructFieldModel
from src.api_model.struct_model import StructModel
from src.generators.generator_interface import GeneratedContent
from src.generators.structs_generator import StructsGenerator, STRUCT_TEMPLATE_FILE_PATH


@patch("src.generators.structs_generator.load_file_content")
class TestStructsGenerator(unittest.TestCase):
    def test_generate_with_no_dependencies(self, load_file_content_mock):
        struct_model_1: StructModel = StructModel(
            name="SomeStruct",
            fields=[
                StructFieldModel(name="SomeField1", type="str"),
                StructFieldModel(name="SomeField2", type="int"),
                StructFieldModel(name="SomeField3", type="float"),
            ],
        )
        struct_model_2: StructModel = StructModel(
            name="AnotherStruct",
            fields=[
                StructFieldModel(name="AnotherField1", type="str"),
                StructFieldModel(name="AnotherField2", type="int"),
                StructFieldModel(name="AnotherField3", type="int"),
            ]
        )
        api_model = MagicMock(
            structs={
                "SomeStruct": struct_model_1,
                "AnotherStruct": struct_model_2
            }
        )
        template: str = "struct_template"
        some_struct_definition: str = "abc"
        another_struct_definition: str = "def"
        expected_output: GeneratedContent = {
            "structs/some_struct.py": some_struct_definition,
            "structs/another_struct.py": another_struct_definition
        }
        empy_interpreter = MagicMock(expand=Mock())

        load_file_content_mock.return_value = template
        empy_interpreter.expand.side_effect = [
            some_struct_definition,
            another_struct_definition
        ]

        output: GeneratedContent = StructsGenerator().generate(empy_interpreter, api_model)

        load_file_content_mock.assert_called_once_with(STRUCT_TEMPLATE_FILE_PATH)
        empy_interpreter.expand.assert_has_calls([
            call(template, {"model": struct_model_1}),
            call(template, {"model": struct_model_2}),
        ])

        for path, content in expected_output.items():
            self.assertTrue(path in output)
            self.assertEqual(output[path], expected_output[path])
