import os
from logging import getLogger

from em import Interpreter

from src.api_model.api_model import ApiModel
from src.generators.generator_interface import GeneratorInterface, GeneratedContent
from src.paths import TEMPLATES_PATH
from src.utils import load_file_content, camel_case_to_snake_case

LOGGER = getLogger("RequestSerializersGenerator")
REQUEST_SERIALIZER_TEMPLATE_FILE_NAME: str = "request_serializer.template"
REQUEST_SERIALIZER_TEMPLATE_FILE_PATH: str = os.path.join(TEMPLATES_PATH, REQUEST_SERIALIZER_TEMPLATE_FILE_NAME)


class RequestSerializersGenerator(GeneratorInterface):
    def generate(self, empy_interpreter: Interpreter, api_model: ApiModel) -> GeneratedContent:
        LOGGER.info(f"Generating request serializers")

        output: GeneratedContent = {}
        template: str = load_file_content(REQUEST_SERIALIZER_TEMPLATE_FILE_PATH)

        for command_model in api_model.commands:
            LOGGER.debug(f"Generating request serializer for {command_model.original_name} commands")

            context: dict = {
                "model": command_model,
                "struct_models": api_model.structs,
            }
            output[self.__get_relative_output_path(command_model.original_name)] = empy_interpreter.expand(template,
                                                                                                           context)

        LOGGER.info(f"Generating of request serializers done")

        return output

    def __get_relative_output_path(self, command_name: str) -> str:
        return os.path.join("request_serializers", f"{camel_case_to_snake_case(command_name)}_request_serializer.py")
