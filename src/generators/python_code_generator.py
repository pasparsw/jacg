from logging import getLogger
from typing import List

from em import Interpreter

from src.api_model.api_model import ApiModel
from src.generators.generator_interface import GeneratedContent, GeneratorInterface

LOGGER = getLogger("PythonCodeGenerator")


class PythonCodeGenerator:
    def __init__(self, empy_interpreter: Interpreter, generators: List[GeneratorInterface]):
        self.__empy_interpreter: Interpreter = empy_interpreter
        self.__generators: List[GeneratorInterface] = generators

    def run(self, api_model: ApiModel) -> GeneratedContent:
        LOGGER.info("Running Python code generators")

        output: GeneratedContent = {}

        for generator in self.__generators:
            output.update(generator.generate(self.__empy_interpreter, api_model))

        LOGGER.info("Running Python code generators done")

        return output
