from dataclasses import dataclass

from typing import List
from ..enums.my_other_enum import MyOtherEnum


@dataclass
class CommandWithEnumsResponse:
    returned_value: List[MyOtherEnum]
