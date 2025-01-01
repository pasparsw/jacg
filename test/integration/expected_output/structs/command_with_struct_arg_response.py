from dataclasses import dataclass

from structs.my_other_struct import MyOtherStruct


@dataclass
class CommandWithStructArgResponse:
    returned_value: MyOtherStruct
