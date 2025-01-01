import unittest

from copy import deepcopy

from src.api_model.struct_field_model import StructFieldModel
from src.api_model.struct_model import StructModel


class TestStructModel(unittest.TestCase):
    def test_struct_model_properties(self):
        inner_dependency: StructModel = StructModel(
            name="InnerDependency",
            fields=[
                StructFieldModel(name="inner_field_1", type="type_1"),
                StructFieldModel(name="inner_field_2", type="type_2"),
            ],
        )
        dependency_1: StructModel = StructModel(
            name="SomeDependency1",
            fields=[
                StructFieldModel(name="dependency_1_field_1", type="InnerDependency"),
                StructFieldModel(name="dependency_1_field_2", type="type_2"),
            ],
            dependencies={
                "InnerDependency": inner_dependency,
            }
        )
        dependency_2: StructModel = StructModel(
            name="SomeDependency2",
            fields=[
                StructFieldModel(name="dependency_2_field_1", type="type_1"),
                StructFieldModel(name="dependency_2_field_2", type="type_2"),
            ],
        )
        model: StructModel = StructModel(
            name="someStruct_name",
            fields=[
                StructFieldModel(name="field_name_1", type="type_1"),
                StructFieldModel(name="field_name_2", type="SomeDependency1"),
                StructFieldModel(name="field_name_3", type="SomeDependency2"),
            ],
            dependencies={
                "SomeDependency1": dependency_1,
                "SomeDependency2": dependency_2,
            }
        )
        other_model = deepcopy(model)
        expected_dependencies = {
            "SomeDependency1": dependency_1,
            "SomeDependency2": dependency_2,
        }
        expected_all_dependencies = {
            "SomeDependency1": dependency_1,
            "InnerDependency": inner_dependency,
            "SomeDependency2": dependency_2,
        }

        self.assertEqual(model.original_name, "someStruct_name")
        self.assertEqual(model, other_model)

        self.assertEqual(model.fields[0].name, "field_name_1")
        self.assertEqual(model.fields[0].type, "type_1")
        self.assertEqual(model.fields[1].name, "field_name_2")
        self.assertEqual(model.fields[1].type, "SomeDependency1")
        self.assertEqual(model.fields[2].name, "field_name_3")
        self.assertEqual(model.fields[2].type, "SomeDependency2")

        self.assertEqual(model.name, "SomeStructName")
        self.assertEqual(model.file_path, "structs/some_struct_name.py")
        self.assertEqual(model.import_path, "structs.some_struct_name")

        self.assertDictEqual(expected_dependencies, model.dependencies)
        self.assertDictEqual(expected_all_dependencies, model.all_dependencies)
