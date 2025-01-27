from dataclasses import dataclass

from typing import List

from ..structs.my_struct import MyStruct
from ..structs.my_other_struct import MyOtherStruct

@dataclass
class MyComplexStruct:
    field_5: MyStruct
    field_6: List[MyOtherStruct]
