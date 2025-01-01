import os
from logging import getLogger

from em import Interpreter

from src.api_model.api_model import ApiModel
from src.generators.generator_interface import GeneratorInterface, GeneratedContent
from src.paths import TEMPLATES_PATH
from src.utils import load_file_content

LOGGER = getLogger("StructsGenerator")
STRUCT_TEMPLATE_FILE_NAME: str = "struct.template"
STRUCT_TEMPLATE_FILE_PATH: str = os.path.join(TEMPLATES_PATH, STRUCT_TEMPLATE_FILE_NAME)


class StructsGenerator(GeneratorInterface):
    def generate(self, empy_interpreter: Interpreter, api_model: ApiModel) -> GeneratedContent:
        LOGGER.info(f"Generating structs definitions")

        output: GeneratedContent = {}
        template: str = load_file_content(STRUCT_TEMPLATE_FILE_PATH)

        for struct_name, struct_model in api_model.structs.items():
            LOGGER.debug(f"Generating definition for {struct_name} struct")

            context: dict = {"model": struct_model}
            output[struct_model.file_path] = empy_interpreter.expand(template, context)

        LOGGER.info(f"Generating of structs definitions done")

        return output
