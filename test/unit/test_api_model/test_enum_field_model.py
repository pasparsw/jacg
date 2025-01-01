import unittest

from copy import deepcopy

from src.api_model.enum_field_model import EnumFieldModel


class TestEnumFieldModel(unittest.TestCase):
    def test_properties(self):
        field_name: str = "SomeName"
        field_value: str = "SomeValue"
        model: EnumFieldModel = EnumFieldModel(
            name=field_name,
            value=field_value
        )
        other_model: EnumFieldModel = deepcopy(model)

        self.assertEqual(model, other_model)
        self.assertEqual(model.name, field_name)
        self.assertEqual(model.value, field_value)
