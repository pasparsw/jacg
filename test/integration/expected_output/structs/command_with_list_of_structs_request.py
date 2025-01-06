from dataclasses import dataclass

from typing import List

from ..structs.my_struct import MyStruct

@dataclass
class CommandWithListOfStructsRequest:
    arg: List[MyStruct]
