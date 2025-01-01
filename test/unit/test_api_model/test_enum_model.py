import unittest

from copy import deepcopy

from src.api_model.enum_field_model import EnumFieldModel
from src.api_model.enum_model import EnumModel


class TestEnumModel(unittest.TestCase):
    def test_enum_model_properties(self):
        model: EnumModel = EnumModel(name="someEnum_name", fields=[
            EnumFieldModel(name="field_name_1", value="1"),
            EnumFieldModel(name="field_name_2", value="2"),
            EnumFieldModel(name="field_name_3", value="3"),
        ])
        other_model: EnumModel = deepcopy(model)

        self.assertEqual(model, other_model)
        self.assertEqual(model.original_name, "someEnum_name")

        self.assertEqual(model.fields[0].name, "field_name_1")
        self.assertEqual(model.fields[0].value, "1")
        self.assertEqual(model.fields[1].name, "field_name_2")
        self.assertEqual(model.fields[1].value, "2")
        self.assertEqual(model.fields[2].name, "field_name_3")
        self.assertEqual(model.fields[2].value, "3")

        self.assertEqual(model.name, "SomeEnumName")
        self.assertEqual(model.file_path, "enums/some_enum_name.py")
        self.assertEqual(model.import_path, "enums.some_enum_name")
