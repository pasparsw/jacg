from abc import abstractmethod
from typing import Dict

from em import Interpreter

from src.api_model.api_model import ApiModel

RelativeFilePath = str
FileContent = str
GeneratedContent = Dict[RelativeFilePath, FileContent]


class GeneratorInterface:
    @abstractmethod
    def generate(self, empy_interpreter: Interpreter, api_model: ApiModel) -> GeneratedContent:
        pass
