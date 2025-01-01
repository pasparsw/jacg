import unittest
from unittest.mock import MagicMock, Mock

from src.generators.generator_interface import GeneratedContent
from src.generators.python_code_generator import PythonCodeGenerator


class TestPythonCodeGenerator(unittest.TestCase):
    def test_run_returns_proper_output(self):
        empy_interpreter = MagicMock()
        api_model = MagicMock()
        generator_1 = MagicMock(generate=Mock())
        generator_2 = MagicMock(generate=Mock())
        generator_3 = MagicMock(generate=Mock())

        generator_1.generate.return_value = {
            "path/1.1": "content_1.1",
            "path/1.2": "content_1.2",
        }
        generator_2.generate.return_value = {
            "path/2.1": "content_2.1",
            "path/2.2": "content_2.2",
        }
        generator_3.generate.return_value = {
            "path/3.1": "content_3.1",
            "path/3.2": "content_3.2",
        }
        expected_output: GeneratedContent = {
            "path/1.1": "content_1.1",
            "path/1.2": "content_1.2",
            "path/2.1": "content_2.1",
            "path/2.2": "content_2.2",
            "path/3.1": "content_3.1",
            "path/3.2": "content_3.2",
        }

        python_code_generator: PythonCodeGenerator = PythonCodeGenerator(empy_interpreter, generators=[generator_1,
                                                                                                       generator_2,
                                                                                                       generator_3])
        output: GeneratedContent = python_code_generator.run(api_model)

        generator_1.generate.assert_called_once_with(empy_interpreter, api_model)
        generator_2.generate.assert_called_once_with(empy_interpreter, api_model)
        generator_3.generate.assert_called_once_with(empy_interpreter, api_model)

        self.assertDictEqual(output, expected_output)
