import unittest

from copy import deepcopy

from src.api_model.struct_field_model import StructFieldModel


class TestStructFieldModel(unittest.TestCase):
    def test_properties_of_simple_field(self):
        field_name: str = "SomeName"
        field_type: str = "SomeType"
        model: StructFieldModel = StructFieldModel(
            name=field_name,
            type=field_type
        )
        other_model: StructFieldModel = deepcopy(model)

        self.assertEqual(model, other_model)
        self.assertEqual(model.name, field_name)
        self.assertEqual(model.type, field_type)
        self.assertFalse(model.is_list())
        self.assertEqual(model.underlying_type, field_type)


    def test_properties_of_list_field(self):
        field_name: str = "SomeName"
        underlying_type: str = "SomeType"
        field_type: str = f"List[{underlying_type}]"
        model: StructFieldModel = StructFieldModel(
            name=field_name,
            type=field_type
        )
        other_model: StructFieldModel = deepcopy(model)

        self.assertEqual(model, other_model)
        self.assertEqual(model.name, field_name)
        self.assertEqual(model.type, field_type)
        self.assertTrue(model.is_list())
        self.assertEqual(model.underlying_type, underlying_type)
