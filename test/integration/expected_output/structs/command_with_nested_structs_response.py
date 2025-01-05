from dataclasses import dataclass

from ..structs.my_complex_struct import MyComplexStruct


@dataclass
class CommandWithNestedStructsResponse:
    returned_value: MyComplexStruct
