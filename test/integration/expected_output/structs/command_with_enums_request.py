from dataclasses import dataclass

from enums.my_enum import MyEnum


@dataclass
class CommandWithEnumsRequest:
    arg: MyEnum
