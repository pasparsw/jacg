import sys
from typing import List

from em import Interpreter

from src.api_model.api_model_creator import ApiModelCreator
from src.commands.run_command_handler import RunCommandHandler
from src.generated_content_writer import GeneratedContentWriter
from src.generators.api_client_generator import ApiClientGenerator
from src.generators.enums_generator import EnumsGenerator
from src.generators.generator_interface import GeneratorInterface
from src.generators.python_code_generator import PythonCodeGenerator
from src.generators.request_serializers_generator import RequestSerializersGenerator
from src.generators.response_deserializers_generator import ResponseDeserializersGenerator
from src.generators.structs_generator import StructsGenerator
from src.jacg_cli import RUN_COMMAND_NAME, API_SPEC_OPTION_NAME, OUTPUT_PATH_OPTION_NAME, LOG_LEVEL_OPTION_NAME, \
    DEFAULT_LOGGING_LEVEL
from thirdparty.comlint_py import CommandLineInterface

GENERATORS: List[GeneratorInterface] = [
    EnumsGenerator(),
    StructsGenerator(),
    RequestSerializersGenerator(),
    ResponseDeserializersGenerator(),
    ApiClientGenerator(),
]


class Jacg:
    def __init__(self):
        self.__cli: CommandLineInterface = CommandLineInterface(argv=sys.argv, program_name="JACG",
                                                                description="JSON API client generators")
        # CLI commands
        self.__cli.add_command(command_name=RUN_COMMAND_NAME, description="Run generation of API Python interface",
                               allowed_options=[API_SPEC_OPTION_NAME, OUTPUT_PATH_OPTION_NAME, LOG_LEVEL_OPTION_NAME],
                               required_options=[API_SPEC_OPTION_NAME, OUTPUT_PATH_OPTION_NAME])

        # CLI options
        self.__cli.add_option(option_name=LOG_LEVEL_OPTION_NAME,
                              description=f"Specify logging level (default: {DEFAULT_LOGGING_LEVEL})",
                              allowed_values=["debug", "info", "warn", "error", "fatal"])
        self.__cli.add_option(option_name=API_SPEC_OPTION_NAME, description="Specify file containing API specification")
        self.__cli.add_option(option_name=OUTPUT_PATH_OPTION_NAME, description="Specify path to directory where"
                                                                               "generated files will be saved")

        self.__api_model_creator: ApiModelCreator = ApiModelCreator()
        self.__empy_interpreter: Interpreter = Interpreter()
        self.__python_code_generator: PythonCodeGenerator = PythonCodeGenerator(self.__empy_interpreter, GENERATORS)
        self.__gen_content_writer: GeneratedContentWriter = GeneratedContentWriter()

        self.__cli.add_command_handler(command_name=RUN_COMMAND_NAME,
                                       command_handler=RunCommandHandler(self.__api_model_creator,
                                                                         self.__python_code_generator,
                                                                         self.__gen_content_writer))

    def run(self) -> None:
        self.__cli.run()
        self.__empy_interpreter.shutdown()
