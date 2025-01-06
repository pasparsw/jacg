import os
from typing import List, Dict

from src.api_model.enum_model import EnumModel
from src.api_model.struct_field_model import StructFieldModel
from src.utils import snake_case_to_camel_case, camel_case_to_snake_case

StructName = str

STRUCTS_DIR_NAME: str = "structs"


class StructModel:
    def __init__(self, name: StructName, fields: List[StructFieldModel], dependencies: Dict[str, any] = None):
        self.original_name: StructName = name
        self.fields: List[StructFieldModel] = fields
        self.dependencies: Dict[str, any] = {} if not dependencies else dependencies

    def __eq__(self, other) -> bool:
        if self.dependencies != other.dependencies:
            return False
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
        return os.path.join(STRUCTS_DIR_NAME, f"{camel_case_to_snake_case(self.original_name)}.py")

    @property
    def import_path(self) -> str:
        return f"{STRUCTS_DIR_NAME}.{camel_case_to_snake_case(self.original_name)}"

    @property
    def has_list_field(self) -> bool:
        for field in self.fields:
            if field.is_list():
                return True
        return False

    @property
    def has_default_empty_list(self) -> bool:
        for field in self.fields:
            if field.is_list() and field.default_value == "[]":
                return True
        return False

    @property
    def all_dependencies(self) -> Dict[str, any]:
        all_deps: Dict[str, any] = {}

        for dependency_name, dependency_model in self.dependencies.items():
            if isinstance(dependency_model, EnumModel):
                all_deps[dependency_name] = dependency_model
            elif dependency_model.dependencies:
                all_deps.update(dependency_model.all_dependencies)

            all_deps[dependency_name] = dependency_model

        return all_deps
