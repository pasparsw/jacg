from dataclasses import dataclass

from typing import List
from ..structs.my_other_struct import MyOtherStruct


@dataclass
class CommandWithListOfStructsResponse:
    returned_value: List[MyOtherStruct]
