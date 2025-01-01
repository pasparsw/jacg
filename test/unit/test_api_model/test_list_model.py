import unittest

from copy import deepcopy

from src.api_model.list_model import ListModel


class TestListModel(unittest.TestCase):
    def test_properties(self):
        model: ListModel = ListModel()
        other_model: ListModel = deepcopy(model)

        self.assertEqual(model, other_model)
        self.assertEqual(model.name, "List")
        self.assertEqual(model.import_path, "typing")
