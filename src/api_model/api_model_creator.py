from logging import getLogger
from typing import List, Dict

from src.api_model.api_model import ApiModel
from src.api_model.command_model import CommandModel
from src.api_model.enum_field_model import EnumFieldModel
from src.api_model.enum_model import EnumModel, EnumName
from src.api_model.list_model import ListModel
from src.api_model.struct_field_model import StructFieldModel
from src.api_model.struct_model import StructName, StructModel
from src.utils import snake_case_to_camel_case

LOGGER = getLogger("ApiModelCreator")


class ApiModelCreator:
    def create(self, api_spec: dict) -> ApiModel:
        LOGGER.info("Creating API model")

        model: ApiModel = ApiModel(name=api_spec["api_name"], hostname=api_spec["hostname"], port=api_spec["port"],
                                   response_buffer_size=api_spec["response_buffer_size"],
                                   response_timeout=api_spec["response_timeout"],
                                   socket_timeout=api_spec["socket_timeout"])

        model.enums = self.__create_enum_models(api_spec["enums"])
        model.structs = self.__create_struct_models(api_spec["structs"], api_spec["commands"])
        model.commands = self.__create_command_models(api_spec["commands"], model.structs)

        self.__resolve_dependencies(model)

        LOGGER.info("API model creation done")

        return model

    def __create_enum_models(self, api_enums_spec: dict) -> Dict[EnumName, EnumModel]:
        LOGGER.info("Creating enum models")

        enum_models: Dict[EnumName, EnumModel] = {}

        for enum_name, enum_spec in api_enums_spec.items():
            LOGGER.debug(f"Creating model for enum {enum_name}")

            enum_fields: List[EnumFieldModel] = []

            for enum_field_name, enum_field_value in enum_spec.items():
                LOGGER.debug(f"Creating enum field for name {enum_field_name} and value {enum_field_value}")
                enum_fields.append(EnumFieldModel(name=enum_field_name, value=enum_field_value))

            enum_models[enum_name] = EnumModel(name=enum_name, fields=enum_fields)

        LOGGER.info("Enum models creation done")

        return enum_models

    def __create_struct_models(self, api_structs_spec: dict, api_commands_spec: dict) -> Dict[StructName, StructModel]:
        LOGGER.info("Creating struct models")

        struct_models: Dict[StructName, StructModel] = {}
        requests_spec: dict = {self.__create_request_name(command_name): command_spec["request"] for
                               command_name, command_spec in api_commands_spec.items()}
        responses_spec: dict = {self.__create_response_name(command_name): command_spec["response"] for
                                command_name, command_spec in api_commands_spec.items()}
        all_structs_spec: dict = {**api_structs_spec, **requests_spec, **responses_spec}

        for struct_name, struct_spec in all_structs_spec.items():
            LOGGER.debug(f"Creating model for struct {struct_name}")

            mandatory_fields: List[StructFieldModel] = []
            optional_fields: List[StructFieldModel] = []

            for struct_field_name, struct_field_type in struct_spec.items():
                LOGGER.debug(f"Creating struct field for name {struct_field_name} and type {struct_field_type}")

                if "=" in struct_field_type:
                    default_field_value: any = struct_field_type.split("=")[1]
                    optional_fields.append(
                        StructFieldModel(name=struct_field_name, type=struct_field_type.split("=")[0],
                                         default_value=default_field_value))
                    LOGGER.debug(f"Field {struct_field_name} has a default value {default_field_value}")
                else:
                    mandatory_fields.append(StructFieldModel(name=struct_field_name, type=struct_field_type))

            struct_models[struct_name] = StructModel(name=struct_name, fields=mandatory_fields + optional_fields)

        LOGGER.info("Struct models creation done")

        return struct_models

    def __create_command_models(self, api_commands_spec: dict,
                                struct_models: Dict[StructName, StructModel]) -> List[CommandModel]:
        LOGGER.info(f"Creating command models")

        command_models: List[CommandModel] = []

        for command_name, command_spec in api_commands_spec.items():
            LOGGER.debug(f"Creating command model for command {command_name}")

            command_models.append(CommandModel(name=command_name,
                                               request=struct_models[self.__create_request_name(command_name)],
                                               response=struct_models[self.__create_response_name(command_name)],
                                               silent=command_spec["silent"]))

        LOGGER.info(f"Command models creation done")

        return command_models

    def __create_request_name(self, command_name: str) -> str:
        return f"{snake_case_to_camel_case(command_name)}Request"

    def __create_response_name(self, command_name: str) -> str:
        return f"{snake_case_to_camel_case(command_name)}Response"

    def __resolve_dependencies(self, model: ApiModel):
        LOGGER.info("Resolving dependencies")

        for struct_name, struct_model in model.structs.items():
            LOGGER.debug(f"Resolving dependencies for {struct_name}")

            for field in struct_model.fields:
                actual_type: str = field.type

                if field.is_list():
                    actual_type = field.underlying_type
                    LOGGER.debug(f"{struct_name} depends on a List of {actual_type}")
                if actual_type in model.enums:
                    LOGGER.debug(f"{struct_name} depends on {actual_type} enum")
                    struct_model.dependencies[actual_type] = model.enums[actual_type]
                if actual_type in model.structs:
                    LOGGER.debug(f"{struct_name} depends on {actual_type} struct")
                    struct_model.dependencies[actual_type] = model.structs[actual_type]

        LOGGER.info("Dependency resolution done")
