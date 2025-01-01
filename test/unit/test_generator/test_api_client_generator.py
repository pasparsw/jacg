import unittest

from unittest.mock import MagicMock, Mock, patch, call

from src.generators.api_client_generator import ApiClientGenerator, API_CLIENT_TEMPLATE_FILE_PATH, JSON_SOCKET_FILE_PATH
from src.generators.generator_interface import GeneratedContent
from src.utils import camel_case_to_snake_case, snake_case_to_camel_case


@patch("src.generators.api_client_generator.load_file_content")
class TestApiClientGenerator(unittest.TestCase):
    def test_generate(self, load_file_content_mock):
        api_model = MagicMock()
        api_model.name = "SomeApi"

        template: str = "api_client.template"
        some_generated_content: str = "abc"
        json_socket_def: str = "json socket definition"
        expected_output: GeneratedContent = {
            "api_client/some_api_client.py": some_generated_content,
            "api_client/json_socket.py": json_socket_def
        }

        empy_interpreter = MagicMock(expand=Mock())

        load_file_content_mock.side_effect = [
            template,
            json_socket_def,
        ]
        empy_interpreter.expand.return_value = some_generated_content

        output: GeneratedContent = ApiClientGenerator().generate(empy_interpreter, api_model)

        load_file_content_mock.assert_has_calls([
            call(API_CLIENT_TEMPLATE_FILE_PATH),
            call(JSON_SOCKET_FILE_PATH),
        ])
        context = {
            "model": api_model,
            "camel_case_to_snake_case": camel_case_to_snake_case,
            "snake_case_to_camel_case": snake_case_to_camel_case,
        }
        empy_interpreter.expand.assert_called_once_with(template, context)

        self.assertDictEqual(output, expected_output)
