import os
from logging import getLogger

from em import Interpreter

from src.api_model.api_model import ApiModel
from src.generators.generator_interface import GeneratorInterface, GeneratedContent
from src.paths import TEMPLATES_PATH, SRC_PATH
from src.utils import load_file_content, camel_case_to_snake_case, snake_case_to_camel_case

LOGGER = getLogger("ApiClientGenerator")
API_CLIENT_TEMPLATE_FILE_NAME: str = "api_client.template"
API_CLIENT_TEMPLATE_FILE_PATH: str = os.path.join(TEMPLATES_PATH, API_CLIENT_TEMPLATE_FILE_NAME)
GENERATED_API_CLIENT_FOLDER_NAME: str = "api_client"


class ApiClientGenerator(GeneratorInterface):
    def generate(self, empy_interpreter: Interpreter, api_model: ApiModel) -> GeneratedContent:
        LOGGER.info(f"Generating API client")

        output: GeneratedContent = {}
        template: str = load_file_content(API_CLIENT_TEMPLATE_FILE_PATH)

        context: dict = {
            "model": api_model,
            "camel_case_to_snake_case": camel_case_to_snake_case,
            "snake_case_to_camel_case": snake_case_to_camel_case,
        }
        output_relative_path: str = os.path.join(GENERATED_API_CLIENT_FOLDER_NAME,
                                                 f"{camel_case_to_snake_case(api_model.name)}_client.py")
        output[output_relative_path] = empy_interpreter.expand(template, context)

        LOGGER.info(f"Generating of API client done")

        return output
