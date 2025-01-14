import os
import unittest
import filecmp

from logging import getLogger

from src.paths import RUN_EXAMPLE_SCRIPT_PATH, EXAMPLE_PATH, REPO_PATH
from src.logger_configurator import LoggerConfigurator
from test.integration.shell_command_runner import ShellCommandRunner

LOGGER = getLogger("JacgIntegrationTest")

EXAMPLE_OUTPUT_DIR_PATH:str = os.path.join(EXAMPLE_PATH, "output")
EXPECTED_OUTPUT_DIR_PATH: str = os.path.join(REPO_PATH, "test", "integration", "expected_output")


class JacgIntegrationTest(unittest.TestCase):
    def test_run_integration_test(self):
        LoggerConfigurator.configure(logging_level_str='debug')

        ShellCommandRunner.execute(f"{RUN_EXAMPLE_SCRIPT_PATH} -log_level debug")

        self.__compare_directories(EXAMPLE_OUTPUT_DIR_PATH, EXPECTED_OUTPUT_DIR_PATH)

        LOGGER.info(f"Integration test finished")

    def __compare_directories(self, dir1, dir2):
        for root1, dirs1, files1 in os.walk(dir1):
            rel_path = os.path.relpath(root1, dir1)
            root2 = os.path.join(dir2, rel_path)

            self.assertTrue(os.path.exists(root2))

            dirs2 = next(os.walk(root2))[1]

            if "__pycache__" in dirs1:
                dirs1.remove("__pycache__")
            if "__pycache__" in dirs2:
                dirs2.remove("__pycache__")

            self.assertEqual(dirs1, dirs2)

            files1 = sorted([f for f in files1 if f.endswith('.py') and "__init__" not in f])
            files2 = sorted([f for f in next(os.walk(root2))[2] if f.endswith('.py') and "__init__" not in f])

            self.assertEqual(files1, files2)

            for file_name in files1:
                file1_path = os.path.join(root1, file_name)
                file2_path = os.path.join(root2, file_name)

                if not filecmp.cmp(file1_path, file2_path, shallow=False):
                    self.fail(f"File {file1_path} is different than file {file2_path}!")

        for root2, dirs2, files2 in os.walk(dir2):
            rel_path = os.path.relpath(root2, dir2)
            root1 = os.path.join(dir1, rel_path)

            self.assertTrue(os.path.exists(root1))
