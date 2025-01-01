import os
from typing import List

from src.api_model.enum_field_model import EnumFieldModel
from src.utils import snake_case_to_camel_case, camel_case_to_snake_case

EnumName = str

ENUMS_DIR_NAME: str = "enums"

class EnumModel:
    def __init__(self, name: EnumName, fields: List[EnumFieldModel]):
        self.original_name: EnumName = name
        self.fields: List[EnumFieldModel] = fields

    def __eq__(self, other) -> bool:
        if len(self.fields) != len(other.fields):
            return False

        for (field, other_field) in zip(self.fields, other.fields):
            if field != other_field:
                return False

        return self.original_name == other.original_name

    @property
    def name(self) -> str:
        return snake_case_to_camel_case(self.original_name)

    @property
    def file_path(self) -> str:
        return os.path.join(ENUMS_DIR_NAME, f"{camel_case_to_snake_case(self.original_name)}.py")

    @property
    def import_path(self) -> str:
        return f"{ENUMS_DIR_NAME}.{camel_case_to_snake_case(self.original_name)}"
