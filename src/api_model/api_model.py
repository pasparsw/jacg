from dataclasses import dataclass, field
from typing import Dict, List

from src.api_connectors.types import Milliseconds
from src.api_model.command_model import CommandModel
from src.api_model.enum_model import EnumModel, EnumName
from src.api_model.struct_model import StructModel, StructName


@dataclass
class ApiModel:
    name: str
    hostname: str
    port: int
    response_buffer_size: int
    response_timeout: Milliseconds
    socket_timeout: Milliseconds
    min_pause_between_requests: Milliseconds
    enums: Dict[EnumName, EnumModel] = field(default_factory=lambda: {})
    structs: Dict[StructName, StructModel] = field(default_factory=lambda: {})
    commands: List[CommandModel] = field(default_factory=lambda: [])
