from typing import Dict

from src.api_model.enum_model import EnumName, EnumModel
from src.api_model.struct_model import StructModel, StructName
from src.utils import camel_case_to_snake_case


def serialize_request_recipe(request: StructModel, struct_models: Dict[StructName, StructModel], indentation_level: int,
                             current_name: str, init_indentation_level: int, end_with_newline=True) -> str:
    indentation: str = "    " * indentation_level
    output: str = "{\n"

    for field in request.fields:
        if field.is_list() and field.underlying_type in struct_models:
            serialized_elements: str = serialize_request_recipe(struct_models[field.underlying_type], struct_models,
                                                                indentation_level + 1, 'element',
                                                                init_indentation_level,
                                                                end_with_newline=False)
            output += (
                f"{indentation}'{field.name}': [{serialized_elements} for element in {current_name}.{field.name}]"
                f",\n")
        elif field.type in struct_models:
            serialized_elements: str = serialize_request_recipe(struct_models[field.type], struct_models,
                                                                indentation_level + 1, f'{current_name}.{field.name}',
                                                                init_indentation_level)
            output += f"{indentation}'{field.name}': {serialized_elements}"
        else:
            output += f"{indentation}'{field.name}': {current_name}.{field.name},\n"

    output += "    " * (indentation_level - 1) + "}"

    if indentation_level > init_indentation_level and end_with_newline:
        output += ","
    if end_with_newline:
        output += "\n"

    return output


def deserialize_response_recipe(response: StructModel, struct_models: Dict[StructName, StructModel],
                                enum_models: Dict[EnumName, EnumModel], indentation_level: int,
                                current_name: str, init_indentation_level: int, end_with_newline: bool = True) -> str:
    indentation: str = "    " * indentation_level
    output: str = f"{response.name}(\n"

    for field in response.fields:
        field_name = field.name
        if field.is_list() and field.underlying_type in struct_models:
            serialized_elements: str = deserialize_response_recipe(struct_models[field.underlying_type], struct_models,
                                                                   enum_models, indentation_level + 1, 'element',
                                                                   init_indentation_level, end_with_newline=False)
            output += (f"{indentation}{field_name}=[{serialized_elements} for element in {current_name}['{field_name}']]"
                       f",\n")
        elif field.type in struct_models:
            serialized_elements: str = deserialize_response_recipe(struct_models[field.type], struct_models,
                                                                   enum_models, indentation_level + 1,
                                                                   f'{current_name}[\'{field_name}\']',
                                                                   init_indentation_level)
            output += f"{indentation}{field_name}={serialized_elements}"
        elif field.type in enum_models:
            output += f"{indentation}{field_name}={field.type}({current_name}['{field_name}']),\n"
        else:
            output += f"{indentation}{field_name}={current_name}['{field_name}'],\n"

    output += "    " * (indentation_level - 1) + ")"

    if indentation_level > init_indentation_level and end_with_newline:
        output += ","
    if end_with_newline:
        output += "\n"

    return output


class CommandModel:
    def __init__(self, name: str, request: StructModel, response: StructModel, silent: bool):
        self.original_name: str = name
        self.request: StructModel = request
        self.response: StructModel = response
        self.is_silent: bool = silent

    def __eq__(self, other) -> bool:
        return self.original_name == other.original_name and \
            self.request == other.request and \
            self.response == other.response

    @property
    def py_function_name(self) -> str:
        return camel_case_to_snake_case(self.original_name)

    def get_request_serialization_recipe(self, struct_models: Dict[StructName, StructModel],
                                         init_indentation_level: int) -> str:
        return serialize_request_recipe(self.request, struct_models, init_indentation_level, "request",
                                        init_indentation_level)

    def get_response_deserialization_recipe(self, struct_models: Dict[StructName, StructModel],
                                            enum_models: Dict[EnumName, EnumModel], init_indentation_level: int) -> str:
        return deserialize_response_recipe(self.response, struct_models, enum_models,
                                           init_indentation_level, "response", init_indentation_level)
