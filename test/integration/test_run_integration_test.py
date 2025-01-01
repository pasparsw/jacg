import os
import unittest

from typing import List
from logging import getLogger

from src.paths import RUN_EXAMPLE_SCRIPT_PATH, EXAMPLE_PATH, REPO_PATH
from src.logger_configurator import LoggerConfigurator
from test.integration.shell_command_runner import ShellCommandRunner

LOGGER = getLogger("JacgIntegrationTest")

EXAMPLE_OUTPUT_DIR_PATH:str = os.path.join(EXAMPLE_PATH, "output")
EXAMPLE_OUTPUT_API_CLIENT_DIR_PATH: str = os.path.join(EXAMPLE_OUTPUT_DIR_PATH, "api_client")
EXAMPLE_OUTPUT_ENUMS_DIR_PATH: str = os.path.join(EXAMPLE_OUTPUT_DIR_PATH, "enums")
EXAMPLE_OUTPUT_REQUEST_SERIALIZERS_DIR_PATH: str = os.path.join(EXAMPLE_OUTPUT_DIR_PATH, "request_serializers")
EXAMPLE_OUTPUT_RESPONSE_DESERIALIZERS_DIR_PATH: str = os.path.join(EXAMPLE_OUTPUT_DIR_PATH, "response_deserializers")
EXAMPLE_OUTPUT_STRUCTS_DIR_PATH: str = os.path.join(EXAMPLE_OUTPUT_DIR_PATH, "structs")

EXPECTED_OUTPUT_DIR_PATH: str = os.path.join(REPO_PATH, "test", "integration", "expected_output")
EXPECTED_OUTPUT_API_CLIENT_DIR_PATH: str = os.path.join(EXPECTED_OUTPUT_DIR_PATH, "api_client")
EXPECTED_OUTPUT_ENUMS_DIR_PATH: str = os.path.join(EXPECTED_OUTPUT_DIR_PATH, "enums")
EXPECTED_OUTPUT_REQUEST_SERIALIZERS_DIR_PATH: str = os.path.join(EXPECTED_OUTPUT_DIR_PATH, "request_serializers")
EXPECTED_OUTPUT_RESPONSE_DESERIALIZERS_DIR_PATH: str = os.path.join(EXPECTED_OUTPUT_DIR_PATH, "response_deserializers")
EXPECTED_OUTPUT_STRUCTS_DIR_PATH: str = os.path.join(EXPECTED_OUTPUT_DIR_PATH, "structs")


class JacgIntegrationTest(unittest.TestCase):
    def test_run_integration_test(self):
        LoggerConfigurator.configure(logging_level_str='debug')

        all_example_output_dir_paths: List[str] = [
            EXPECTED_OUTPUT_API_CLIENT_DIR_PATH,
            EXPECTED_OUTPUT_ENUMS_DIR_PATH,
            EXPECTED_OUTPUT_REQUEST_SERIALIZERS_DIR_PATH,
            EXPECTED_OUTPUT_RESPONSE_DESERIALIZERS_DIR_PATH,
            EXPECTED_OUTPUT_STRUCTS_DIR_PATH
        ]

        ShellCommandRunner.execute(f"{RUN_EXAMPLE_SCRIPT_PATH} -log_level debug")

        LOGGER.info(f"Checking if all the expected directories exist in the generated example output")
        for example_output_dir_path in all_example_output_dir_paths:
            if not os.path.exists(example_output_dir_path):
                raise RuntimeError(f"After running example one of the example output directories does not exist in "
                                   f"the expected path: {example_output_dir_path}")

        LOGGER.info(f"Reading files from the generated example output")

        example_output_api_client_file_paths: List[str] = [path for path in os.listdir(EXAMPLE_OUTPUT_API_CLIENT_DIR_PATH)]
        example_output_enums_file_paths: List[str] = [path for path in os.listdir(EXAMPLE_OUTPUT_ENUMS_DIR_PATH)]
        example_output_request_serializers_file_paths: List[str] = [path for path in os.listdir(EXAMPLE_OUTPUT_REQUEST_SERIALIZERS_DIR_PATH)]
        example_output_response_deserializers_file_paths: List[str] = [path for path in os.listdir(EXAMPLE_OUTPUT_RESPONSE_DESERIALIZERS_DIR_PATH)]
        example_output_structs_file_paths: List[str] = [path for path in os.listdir(EXAMPLE_OUTPUT_STRUCTS_DIR_PATH)]

        LOGGER.info(f"Reading files from the expected generated output")

        expected_output_api_client_file_paths: List[str] = [path for path in os.listdir(EXPECTED_OUTPUT_API_CLIENT_DIR_PATH)]
        expected_output_enums_file_paths: List[str] = [path for path in os.listdir(EXPECTED_OUTPUT_ENUMS_DIR_PATH)]
        expected_output_request_serializers_file_paths: List[str] = [path for path in os.listdir(EXPECTED_OUTPUT_REQUEST_SERIALIZERS_DIR_PATH)]
        expected_output_response_deserializers_file_paths: List[str] = [path for path in os.listdir(EXPECTED_OUTPUT_RESPONSE_DESERIALIZERS_DIR_PATH)]
        expected_output_structs_file_paths: List[str] = [path for path in os.listdir(EXPECTED_OUTPUT_STRUCTS_DIR_PATH)]

        LOGGER.info(f"Comparing number of files in each of the expected output directories")

        self.assertEqual(len(example_output_api_client_file_paths), len(expected_output_api_client_file_paths))
        self.assertEqual(len(example_output_enums_file_paths), len(expected_output_enums_file_paths))
        self.assertEqual(len(example_output_request_serializers_file_paths), len(expected_output_request_serializers_file_paths))
        self.assertEqual(len(example_output_response_deserializers_file_paths), len(expected_output_response_deserializers_file_paths))
        self.assertEqual(len(example_output_structs_file_paths), len(expected_output_structs_file_paths))

        LOGGER.info(f"Checking generated files content in {EXAMPLE_OUTPUT_API_CLIENT_DIR_PATH}")

        for example_output_file_path, expected_output_file_path in zip(example_output_api_client_file_paths, expected_output_api_client_file_paths):
            with open(os.path.join(EXAMPLE_OUTPUT_API_CLIENT_DIR_PATH, example_output_file_path)) as example_output_file:
                with open(os.path.join(EXPECTED_OUTPUT_API_CLIENT_DIR_PATH, expected_output_file_path)) as expected_output_file:
                    self.assertEqual(example_output_file.read(), expected_output_file.read())

        LOGGER.info(f"Checking generated files content in {EXAMPLE_OUTPUT_ENUMS_DIR_PATH}")

        for example_output_file_path, expected_output_file_path in zip(example_output_enums_file_paths, expected_output_enums_file_paths):
            with open(os.path.join(EXAMPLE_OUTPUT_ENUMS_DIR_PATH, example_output_file_path)) as example_output_file:
                with open(os.path.join(EXPECTED_OUTPUT_ENUMS_DIR_PATH, expected_output_file_path)) as expected_output_file:
                    self.assertEqual(example_output_file.read(), expected_output_file.read())

        LOGGER.info(f"Checking generated files content in {EXAMPLE_OUTPUT_REQUEST_SERIALIZERS_DIR_PATH}")

        for example_output_file_path, expected_output_file_path in zip(example_output_request_serializers_file_paths, expected_output_request_serializers_file_paths):
            with open(os.path.join(EXAMPLE_OUTPUT_REQUEST_SERIALIZERS_DIR_PATH, example_output_file_path)) as example_output_file:
                with open(os.path.join(EXPECTED_OUTPUT_REQUEST_SERIALIZERS_DIR_PATH, expected_output_file_path)) as expected_output_file:
                    self.assertEqual(example_output_file.read(), expected_output_file.read())

        LOGGER.info(f"Checking generated files content in {EXAMPLE_OUTPUT_RESPONSE_DESERIALIZERS_DIR_PATH}")

        for example_output_file_path, expected_output_file_path in zip(example_output_response_deserializers_file_paths, expected_output_response_deserializers_file_paths):
            with open(os.path.join(EXAMPLE_OUTPUT_RESPONSE_DESERIALIZERS_DIR_PATH, example_output_file_path)) as example_output_file:
                with open(os.path.join(EXPECTED_OUTPUT_RESPONSE_DESERIALIZERS_DIR_PATH, expected_output_file_path)) as expected_output_file:
                    self.assertEqual(example_output_file.read(), expected_output_file.read())

        LOGGER.info(f"Checking generated files content in {EXAMPLE_OUTPUT_STRUCTS_DIR_PATH}")

        for example_output_file_path, expected_output_file_path in zip(example_output_structs_file_paths, expected_output_structs_file_paths):
            with open(os.path.join(EXAMPLE_OUTPUT_STRUCTS_DIR_PATH, example_output_file_path)) as example_output_file:
                with open(os.path.join(EXPECTED_OUTPUT_STRUCTS_DIR_PATH, expected_output_file_path)) as expected_output_file:
                    self.assertEqual(example_output_file.read(), expected_output_file.read())

        LOGGER.info(f"Integration test finished")
