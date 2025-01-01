from dataclasses import dataclass

from enums.my_other_enum import MyOtherEnum


@dataclass
class CommandWithEnumsResponse:
    returned_value: MyOtherEnum
