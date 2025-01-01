from logging import getLogger

from src.api_model.api_model import ApiModel
from src.api_model.api_model_creator import ApiModelCreator
from src.generated_content_writer import GeneratedContentWriter
from src.generators.python_code_generator import PythonCodeGenerator, GeneratedContent
from src.logger_configurator import LoggerConfigurator
from thirdparty.comlint_py import CommandHandlerInterface, ParsedCommand
from src.jacg_cli import API_SPEC_OPTION_NAME, OUTPUT_PATH_OPTION_NAME, LOG_LEVEL_OPTION_NAME, DEFAULT_LOGGING_LEVEL
from src.utils import load_json

LOGGER = getLogger("RunCommandHandler")


class RunCommandHandler(CommandHandlerInterface):
    def __init__(self, api_model_creator: ApiModelCreator, python_code_generator: PythonCodeGenerator, gen_content_writer: GeneratedContentWriter):
        self.__api_mode_creator: ApiModelCreator = api_model_creator
        self.__python_code_generator: PythonCodeGenerator = python_code_generator
        self.__gen_content_writer: GeneratedContentWriter = gen_content_writer

    def run(self, command: ParsedCommand) -> None:
        if command.is_option_used(LOG_LEVEL_OPTION_NAME):
            LoggerConfigurator.configure(logging_level_str=command.options[LOG_LEVEL_OPTION_NAME])
        else:
            LoggerConfigurator.configure(logging_level_str=DEFAULT_LOGGING_LEVEL)

        api_spec_path: str = command.options[API_SPEC_OPTION_NAME]
        output_path: str = command.options[OUTPUT_PATH_OPTION_NAME]

        LOGGER.info(f'Running JACG for API defined in {api_spec_path}')

        api_spec: dict = load_json(api_spec_path)
        api_model: ApiModel = self.__api_mode_creator.create(api_spec)
        generated_content: GeneratedContent = self.__python_code_generator.run(api_model)

        self.__gen_content_writer.write(output_path, generated_content)

        LOGGER.info(f"Run command done")
