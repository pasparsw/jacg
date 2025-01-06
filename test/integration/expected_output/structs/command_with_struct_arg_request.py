from dataclasses import dataclass


from ..structs.my_struct import MyStruct

@dataclass
class CommandWithStructArgRequest:
    arg: MyStruct
