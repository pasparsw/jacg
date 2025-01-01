import os
from logging import getLogger

from em import Interpreter

from src.api_model.api_model import ApiModel
from src.generators.generator_interface import GeneratorInterface, GeneratedContent
from src.paths import TEMPLATES_PATH
from src.utils import load_file_content

LOGGER = getLogger("EnumsGenerator")
ENUM_TEMPLATE_FILE_NAME: str = "enum.template"
ENUM_TEMPLATE_FILE_PATH: str = os.path.join(TEMPLATES_PATH, ENUM_TEMPLATE_FILE_NAME)


class EnumsGenerator(GeneratorInterface):
    def generate(self, empy_interpreter: Interpreter, api_model: ApiModel) -> GeneratedContent:
        LOGGER.info(f"Generating enums definitions")

        output: GeneratedContent = {}
        template: str = load_file_content(ENUM_TEMPLATE_FILE_PATH)

        for enum_name, enum_model in api_model.enums.items():
            LOGGER.debug(f"Generating definition for {enum_name} enum")

            context: dict = {"model": enum_model}
            output[enum_model.file_path] = empy_interpreter.expand(template, context)

        LOGGER.info(f"Generating of enums definitions done")

        return output
