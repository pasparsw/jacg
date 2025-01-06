import os
import shutil
import stat

from logging import getLogger

from src.generators.python_code_generator import GeneratedContent
from src.paths import SRC_PATH
from src.utils import save_to_file

LOGGER = getLogger("GeneratedContentWriter")

API_CONNECTORS_DIR_NAME: str = "api_connectors"
EXCEPTIONS_DIR_NAME: str = "exceptions"
API_CONNECTORS_DIR_PATH: str = os.path.join(SRC_PATH, API_CONNECTORS_DIR_NAME)
EXCEPTIONS_DIR_PATH: str = os.path.join(SRC_PATH, EXCEPTIONS_DIR_NAME)


def read_only_remove_handler(func, path, exc_info):
    os.chmod(path, stat.S_IWRITE)
    os.unlink(path)


class GeneratedContentWriter:
    def write(self, output_path: str, generated_content: GeneratedContent) -> None:
        LOGGER.info(f"Saving generated content to {output_path}")

        for path, content in generated_content.items():
            full_output_path: str = os.path.join(output_path, path)
            dir_path: str = os.path.dirname(full_output_path)

            if not os.path.exists(dir_path):
                os.makedirs(dir_path)
                with open(os.path.join(dir_path, "__init__.py"), 'w') as file:
                    file.write("")

            save_to_file(full_output_path, content)

        api_connectors_target_path: str = os.path.join(output_path, API_CONNECTORS_DIR_NAME)

        if os.path.exists(api_connectors_target_path):
            shutil.rmtree(api_connectors_target_path, onerror=read_only_remove_handler)

        shutil.copytree(API_CONNECTORS_DIR_PATH, api_connectors_target_path)

        exceptions_target_path: str = os.path.join(output_path, EXCEPTIONS_DIR_NAME)

        if os.path.exists(exceptions_target_path):
            shutil.rmtree(exceptions_target_path, onerror=read_only_remove_handler)

        shutil.copytree(EXCEPTIONS_DIR_PATH, exceptions_target_path)

        LOGGER.info("Saving of the generated content done")
