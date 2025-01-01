import unittest
from copy import deepcopy
from typing import Dict

from src.api_model.command_model import CommandModel
from src.api_model.struct_field_model import StructFieldModel
from src.api_model.struct_model import StructModel, StructName


class TestCommandModel(unittest.TestCase):
    def test_get_request_serialization_recipe_for_simple_request(self):
        request_struct: StructModel = StructModel(
            name="RequestStruct",
            fields=[
                StructFieldModel(name="Field1", type="int"),
                StructFieldModel(name="Field2", type="str"),
                StructFieldModel(name="Field3", type="float"),
            ]
        )
        struct_models: Dict[StructName, StructModel] = {
            "RequestStruct": request_struct,
        }
        model: CommandModel = CommandModel(name="SomeCommand",
                                           request=request_struct,
                                           response=StructModel(name="NotImportant", fields=[]),
                                           silent=False)
        expected_recipe: str = \
"""{
    'Field1': request.Field1,
    'Field2': request.Field2,
    'Field3': request.Field3,
}
"""
        recipe: str = model.get_request_serialization_recipe(struct_models, init_indentation_level=1)

        self.assertEqual(recipe, expected_recipe)

    def test_get_request_serialization_recipe_for_request_with_list_of_primitives(self):
        request_struct: StructModel = StructModel(
            name="RequestStruct",
            fields=[
                StructFieldModel(name="Field1", type="List[int]"),
                StructFieldModel(name="Field2", type="str"),
                StructFieldModel(name="Field3", type="float"),
            ]
        )
        struct_models: Dict[StructName, StructModel] = {
            "RequestStruct": request_struct,
        }
        model: CommandModel = CommandModel(name="SomeCommand",
                                           request=request_struct,
                                           response=StructModel(name="NotImportant", fields=[]),
                                           silent=False)
        expected_recipe: str = \
"""{
    'Field1': request.Field1,
    'Field2': request.Field2,
    'Field3': request.Field3,
}
"""
        recipe: str = model.get_request_serialization_recipe(struct_models, init_indentation_level=1)

        self.assertEqual(recipe, expected_recipe)

    def test_get_request_serialization_recipe_for_request_with_list_of_structs(self):
        dependency: StructModel = StructModel(
            name="DependencyStruct",
            fields=[
                StructFieldModel(name="Field4", type="str"),
                StructFieldModel(name="Field5", type="float"),
            ]
        )
        request_struct: StructModel = StructModel(
            name="RequestStruct",
            fields=[
                StructFieldModel(name="Field1", type="str"),
                StructFieldModel(name="Field2", type="List[DependencyStruct]"),
                StructFieldModel(name="Field3", type="float"),
            ],
            dependencies={
                "DependencyStruct": dependency,
            }
        )
        struct_models: Dict[StructName, StructModel] = {
            "RequestStruct": request_struct,
            "DependencyStruct": dependency
        }
        model: CommandModel = CommandModel(name="SomeCommand",
                                           request=request_struct,
                                           response=StructModel(name="NotImportant", fields=[]),
                                           silent=False)
        expected_recipe: str = \
"""{
    'Field1': request.Field1,
    'Field2': [{
        'Field4': element.Field4,
        'Field5': element.Field5,
    } for element in request.Field2],
    'Field3': request.Field3,
}
"""
        recipe: str = model.get_request_serialization_recipe(struct_models, init_indentation_level=1)

        self.assertEqual(recipe, expected_recipe)

    def test_get_request_serialization_recipe_for_request_with_dependency_to_another_struct(self):
        dependency: StructModel = StructModel(
            name="DependencyStruct",
            fields=[
                StructFieldModel(name="Field4", type="str"),
                StructFieldModel(name="Field5", type="float"),
            ]
        )
        request_struct: StructModel = StructModel(
            name="RequestStruct",
            fields=[
                StructFieldModel(name="Field1", type="str"),
                StructFieldModel(name="Field2", type="DependencyStruct"),
                StructFieldModel(name="Field3", type="float"),
            ],
            dependencies={
                "DependencyStruct": dependency,
            }
        )
        struct_models: Dict[StructName, StructModel] = {
            "RequestStruct": request_struct,
            "DependencyStruct": dependency
        }
        model: CommandModel = CommandModel(name="SomeCommand",
                                           request=request_struct,
                                           response=StructModel(name="NotImportant", fields=[]),
                                           silent=False)
        expected_recipe: str = \
"""{
    'Field1': request.Field1,
    'Field2': {
        'Field4': request.Field2.Field4,
        'Field5': request.Field2.Field5,
    },
    'Field3': request.Field3,
}
"""
        recipe: str = model.get_request_serialization_recipe(struct_models, init_indentation_level=1)

        self.assertEqual(recipe, expected_recipe)

    def test_get_request_serialization_recipe_for_request_with_multiple_nested_dependencies(self):
        struct_1: StructModel = StructModel(
            name="Struct1",
            fields=[
                StructFieldModel(name="Field_1_1", type="str"),
                StructFieldModel(name="Field_1_2", type="float"),
            ]
        )
        struct_2: StructModel = StructModel(
            name="Struct2",
            fields=[
                StructFieldModel(name="Field_2_1", type="str"),
                StructFieldModel(name="Field_2_2", type="float"),
            ]
        )
        struct_3: StructModel = StructModel(
            name="Struct3",
            fields=[
                StructFieldModel(name="Field_3_1", type="str"),
                StructFieldModel(name="Field_3_2", type="float"),
            ]
        )
        struct_4: StructModel = StructModel(
            name="Struct4",
            fields=[
                StructFieldModel(name="Field_4_1", type="str"),
                StructFieldModel(name="Field_4_2", type="int"),
            ]
        )
        struct_5: StructModel = StructModel(
            name="Struct5",
            fields=[
                StructFieldModel(name="Field_5_1", type="Struct3"),
                StructFieldModel(name="Field_5_2", type="Struct4"),
            ],
            dependencies={
                "Struct3": struct_3,
                "Struct4": struct_4,
            }
        )
        request_struct: StructModel = StructModel(
            name="RequestStruct",
            fields=[
                StructFieldModel(name="Field_r1", type="Struct1"),        # dependency to a structure
                StructFieldModel(name="Field_r2", type="List[Struct2]"),  # dependency to a list of structures
                StructFieldModel(name="Field_r3", type="Struct5"),        # dependency to a structure with other deps
                StructFieldModel(name="Field_r4", type="float"),
            ],
            dependencies={
                "Struct1": struct_1,
                "Struct2": struct_2,
                "Struct5": struct_5,
            }
        )
        struct_models: Dict[StructName, StructModel] = {
            "RequestStruct": request_struct,
            "Struct1": struct_1,
            "Struct2": struct_2,
            "Struct3": struct_3,
            "Struct4": struct_4,
            "Struct5": struct_5,
        }
        model: CommandModel = CommandModel(name="SomeCommand",
                                           request=request_struct,
                                           response=StructModel(name="NotImportant", fields=[]),
                                           silent=False)
        expected_recipe: str = \
"""{
    'Field_r1': {
        'Field_1_1': request.Field_r1.Field_1_1,
        'Field_1_2': request.Field_r1.Field_1_2,
    },
    'Field_r2': [{
        'Field_2_1': element.Field_2_1,
        'Field_2_2': element.Field_2_2,
    } for element in request.Field_r2],
    'Field_r3': {
        'Field_5_1': {
            'Field_3_1': request.Field_r3.Field_5_1.Field_3_1,
            'Field_3_2': request.Field_r3.Field_5_1.Field_3_2,
        },
        'Field_5_2': {
            'Field_4_1': request.Field_r3.Field_5_2.Field_4_1,
            'Field_4_2': request.Field_r3.Field_5_2.Field_4_2,
        },
    },
    'Field_r4': request.Field_r4,
}
"""
        recipe: str = model.get_request_serialization_recipe(struct_models, init_indentation_level=1)

        self.assertEqual(recipe, expected_recipe)

    def test_get_response_deserialization_recipe_for_simple_response(self):
        response_struct: StructModel = StructModel(
            name="ResponseStruct",
            fields=[
                StructFieldModel(name="Field1", type="int"),
                StructFieldModel(name="Field2", type="str"),
                StructFieldModel(name="Field3", type="float"),
            ]
        )
        struct_models: Dict[StructName, StructModel] = {
            "ResponseStruct": response_struct,
        }
        model: CommandModel = CommandModel(name="SomeCommand",
                                           request=StructModel(name="NotImportant", fields=[]),
                                           response=response_struct,
                                           silent=False)
        expected_recipe: str = \
"""ResponseStruct(
    Field1=response['Field1'],
    Field2=response['Field2'],
    Field3=response['Field3'],
)
"""
        recipe: str = model.get_response_deserialization_recipe(struct_models, {}, init_indentation_level=1)

        self.assertEqual(recipe, expected_recipe)

    def test_get_response_deserialization_recipe_for_response_with_list_of_primitives(self):
        response_struct: StructModel = StructModel(
            name="ResponseStruct",
            fields=[
                StructFieldModel(name="Field1", type="List[int]"),
                StructFieldModel(name="Field2", type="str"),
                StructFieldModel(name="Field3", type="float"),
            ]
        )
        struct_models: Dict[StructName, StructModel] = {
            "ResponseStruct": response_struct,
        }
        model: CommandModel = CommandModel(name="SomeCommand",
                                           request=StructModel(name="NotImportant", fields=[]),
                                           response=response_struct,
                                           silent=False)
        expected_recipe: str = \
"""ResponseStruct(
    Field1=response['Field1'],
    Field2=response['Field2'],
    Field3=response['Field3'],
)
"""
        recipe: str = model.get_response_deserialization_recipe(struct_models, {}, init_indentation_level=1)

        self.assertEqual(recipe, expected_recipe)

    def test_get_response_deserialization_recipe_for_response_with_list_of_structs(self):
        dependency: StructModel = StructModel(
            name="DependencyStruct",
            fields=[
                StructFieldModel(name="Field4", type="str"),
                StructFieldModel(name="Field5", type="float"),
            ]
        )
        response_struct: StructModel = StructModel(
            name="ResponseStruct",
            fields=[
                StructFieldModel(name="Field1", type="str"),
                StructFieldModel(name="Field2", type="List[DependencyStruct]"),
                StructFieldModel(name="Field3", type="float"),
            ],
            dependencies={
                "DependencyStruct": dependency,
            }
        )
        struct_models: Dict[StructName, StructModel] = {
            "ResponseStruct": response_struct,
            "DependencyStruct": dependency
        }
        model: CommandModel = CommandModel(name="SomeCommand",
                                           request=StructModel(name="NotImportant", fields=[]),
                                           response=response_struct,
                                           silent=False)
        expected_recipe: str = \
"""ResponseStruct(
    Field1=response['Field1'],
    Field2=[DependencyStruct(
        Field4=element['Field4'],
        Field5=element['Field5'],
    ) for element in response['Field2']],
    Field3=response['Field3'],
)
"""
        recipe: str = model.get_response_deserialization_recipe(struct_models, {}, init_indentation_level=1)

        self.assertEqual(recipe, expected_recipe)

    def test_get_response_deserialization_recipe_for_response_with_dependency_to_another_struct(self):
        dependency: StructModel = StructModel(
            name="DependencyStruct",
            fields=[
                StructFieldModel(name="Field4", type="str"),
                StructFieldModel(name="Field5", type="float"),
            ]
        )
        response_struct: StructModel = StructModel(
            name="ResponseStruct",
            fields=[
                StructFieldModel(name="Field1", type="str"),
                StructFieldModel(name="Field2", type="DependencyStruct"),
                StructFieldModel(name="Field3", type="float"),
            ],
            dependencies={
                "DependencyStruct": dependency,
            }
        )
        struct_models: Dict[StructName, StructModel] = {
            "ResponseStruct": response_struct,
            "DependencyStruct": dependency
        }
        model: CommandModel = CommandModel(name="SomeCommand",
                                           request=StructModel(name="NotImportant", fields=[]),
                                           response=response_struct,
                                           silent=False)
        expected_recipe: str = \
"""ResponseStruct(
    Field1=response['Field1'],
    Field2=DependencyStruct(
        Field4=response['Field2']['Field4'],
        Field5=response['Field2']['Field5'],
    ),
    Field3=response['Field3'],
)
"""
        recipe: str = model.get_response_deserialization_recipe(struct_models, {}, init_indentation_level=1)

        self.assertEqual(recipe, expected_recipe)

    def test_get_response_deserialization_recipe_for_response_with_multiple_nested_dependencies(self):
        struct_1: StructModel = StructModel(
            name="Struct1",
            fields=[
                StructFieldModel(name="Field_1_1", type="str"),
                StructFieldModel(name="Field_1_2", type="float"),
            ]
        )
        struct_2: StructModel = StructModel(
            name="Struct2",
            fields=[
                StructFieldModel(name="Field_2_1", type="str"),
                StructFieldModel(name="Field_2_2", type="float"),
            ]
        )
        struct_3: StructModel = StructModel(
            name="Struct3",
            fields=[
                StructFieldModel(name="Field_3_1", type="str"),
                StructFieldModel(name="Field_3_2", type="float"),
            ]
        )
        struct_4: StructModel = StructModel(
            name="Struct4",
            fields=[
                StructFieldModel(name="Field_4_1", type="str"),
                StructFieldModel(name="Field_4_2", type="int"),
            ]
        )
        struct_5: StructModel = StructModel(
            name="Struct5",
            fields=[
                StructFieldModel(name="Field_5_1", type="Struct3"),
                StructFieldModel(name="Field_5_2", type="Struct4"),
            ],
            dependencies={
                "Struct3": struct_3,
                "Struct4": struct_4,
            }
        )
        response_struct: StructModel = StructModel(
            name="ResponseStruct",
            fields=[
                StructFieldModel(name="Field_r1", type="Struct1"),  # dependency to a structure
                StructFieldModel(name="Field_r2", type="List[Struct2]"),  # dependency to a list of structures
                StructFieldModel(name="Field_r3", type="Struct5"),  # dependency to a structure with other deps
                StructFieldModel(name="Field_r4", type="float"),
            ],
            dependencies={
                "Struct1": struct_1,
                "Struct2": struct_2,
                "Struct5": struct_5,
            }
        )
        struct_models: Dict[StructName, StructModel] = {
            "ResponseStruct": response_struct,
            "Struct1": struct_1,
            "Struct2": struct_2,
            "Struct3": struct_3,
            "Struct4": struct_4,
            "Struct5": struct_5,
        }
        model: CommandModel = CommandModel(name="SomeCommand",
                                           request=StructModel(name="NotImportant", fields=[]),
                                           response=response_struct,
                                           silent=False)
        expected_recipe: str = \
"""ResponseStruct(
    Field_r1=Struct1(
        Field_1_1=response['Field_r1']['Field_1_1'],
        Field_1_2=response['Field_r1']['Field_1_2'],
    ),
    Field_r2=[Struct2(
        Field_2_1=element['Field_2_1'],
        Field_2_2=element['Field_2_2'],
    ) for element in response['Field_r2']],
    Field_r3=Struct5(
        Field_5_1=Struct3(
            Field_3_1=response['Field_r3']['Field_5_1']['Field_3_1'],
            Field_3_2=response['Field_r3']['Field_5_1']['Field_3_2'],
        ),
        Field_5_2=Struct4(
            Field_4_1=response['Field_r3']['Field_5_2']['Field_4_1'],
            Field_4_2=response['Field_r3']['Field_5_2']['Field_4_2'],
        ),
    ),
    Field_r4=response['Field_r4'],
)
"""
        recipe: str = model.get_response_deserialization_recipe(struct_models, {}, init_indentation_level=1)
        other_model: CommandModel = deepcopy(model)

        self.assertEqual(recipe, expected_recipe)
        self.assertEqual(model, other_model)
