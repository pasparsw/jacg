import unittest

from unittest.mock import MagicMock, Mock, patch

from src.commands.run_command_handler import RunCommandHandler
from thirdparty.comlint_py import CommandHandlerInterface


class TestRunCommandHandler(unittest.TestCase):
    @patch("src.commands.run_command_handler.load_json")
    def test_run_calls_proper_functions(self, load_json_mock):
        api_spec = dict
        api_model = MagicMock()
        generated_content = {}
        path_to_spec: str = "path/to/spec.json"
        output_path: str = "some/output/path"
        parsed_command = MagicMock(options={"-spec": path_to_spec,
                                            "-output": output_path},
                                   is_option_used=Mock())

        api_model_creator = MagicMock(create=Mock())
        python_code_generator = MagicMock(run=Mock())
        generated_content_writer = MagicMock(write=Mock())

        load_json_mock.return_value = api_spec
        api_model_creator.create.return_value = api_model
        python_code_generator.run.return_value = generated_content
        parsed_command.is_option_used.return_value = False

        command: CommandHandlerInterface = RunCommandHandler(api_model_creator, python_code_generator,
                                                             generated_content_writer)

        command.run(parsed_command)

        load_json_mock.assert_called_once_with(path_to_spec)
        api_model_creator.create.assert_called_once_with(api_spec)
        python_code_generator.run.assert_called_once_with(api_model)
        generated_content_writer.write.assert_called_once_with(output_path, generated_content)
