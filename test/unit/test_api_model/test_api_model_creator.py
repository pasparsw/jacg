import unittest

from src.api_model.api_model import ApiModel
from src.api_model.api_model_creator import ApiModelCreator
from src.api_model.command_model import CommandModel
from src.api_model.enum_field_model import EnumFieldModel
from src.api_model.enum_model import EnumModel
from src.api_model.list_model import ListModel
from src.api_model.struct_field_model import StructFieldModel
from src.api_model.struct_model import StructModel


class TestApiModelCreator(unittest.TestCase):
    def test_create_enums_only(self):
        api_spec: dict = {
            "api_name": "ApiName",
            "hostname": "api.hostname",
            "port": 1234,
            "response_buffer_size": 1024,
            "timeout": 5,
            "ssl": False,
            "enums": {
                "SomeEnum": {
                    "SomeEnumField1": "0",
                    "SomeEnumField2": "1",
                    "SomeEnumField3": "2",
                },
                "AnotherEnum": {
                    "AnotherEnumField1": "0",
                    "AnotherEnumField2": "1",
                    "AnotherEnumField3": "2",
                }
            },
            "structs": {},
            "commands": {},
        }

        expected_model: ApiModel = ApiModel(
            name="ApiName",
            hostname="api.hostname",
            port=1234,
            response_buffer_size=1024,
            timeout=5,
            ssl=False,
            enums={
                "SomeEnum": EnumModel(
                    name="SomeEnum",
                    fields=[
                        EnumFieldModel(name="SomeEnumField1", value="0"),
                        EnumFieldModel(name="SomeEnumField2", value="1"),
                        EnumFieldModel(name="SomeEnumField3", value="2"),
                    ]
                ),
                "AnotherEnum": EnumModel(
                    name="AnotherEnum",
                    fields=[
                        EnumFieldModel(name="AnotherEnumField1", value="0"),
                        EnumFieldModel(name="AnotherEnumField2", value="1"),
                        EnumFieldModel(name="AnotherEnumField3", value="2"),
                    ]
                )
            },
            structs={},
            commands=[]
        )

        output: ApiModel = ApiModelCreator().create(api_spec)

        self.assertEqual(output, expected_model)

    def test_create_structs_only_with_primitive_types_only(self):
        api_spec: dict = {
            "api_name": "ApiName",
            "hostname": "api.hostname",
            "port": 1234,
            "response_buffer_size": 1024,
            "timeout": 5,
            "ssl": False,
            "enums": {},
            "structs": {
                "SomeStruct": {
                    "SomeField1": "str",
                    "SomeField2": "int",
                    "SomeField3": "float",
                },
                "AnotherStruct": {
                    "AnotherField1": "str",
                    "AnotherField2": "int",
                    "AnotherField3": "float",
                }
            },
            "commands": {},
        }

        expected_model: ApiModel = ApiModel(
            name="ApiName",
            hostname="api.hostname",
            port=1234,
            response_buffer_size=1024,
            timeout=5,
            ssl=False,
            enums={},
            structs={
                "SomeStruct": StructModel(
                    name="SomeStruct",
                    fields=[
                        StructFieldModel(name="SomeField1", type="str"),
                        StructFieldModel(name="SomeField2", type="int"),
                        StructFieldModel(name="SomeField3", type="float"),
                    ]
                ),
                "AnotherStruct": StructModel(
                    name="AnotherStruct",
                    fields=[
                        StructFieldModel(name="AnotherField1", type="str"),
                        StructFieldModel(name="AnotherField2", type="int"),
                        StructFieldModel(name="AnotherField3", type="float"),
                    ]
                )
            },
            commands=[]
        )

        output: ApiModel = ApiModelCreator().create(api_spec)

        self.assertEqual(output, expected_model)

    def test_create_structs_only_with_fields_having_default_values(self):
        api_spec: dict = {
            "api_name": "ApiName",
            "hostname": "api.hostname",
            "port": 1234,
            "response_buffer_size": 1024,
            "timeout": 5,
            "ssl": False,
            "enums": {},
            "structs": {
                "SomeStruct": {
                    "SomeField1": "str='some default string value'",
                    "SomeField2": "int",
                    "SomeField3": "float=3.14",
                },
                "AnotherStruct": {
                    "AnotherField1": "str",
                    "AnotherField2": "int=12",
                    "AnotherField3": "float",
                }
            },
            "commands": {},
        }

        expected_model: ApiModel = ApiModel(
            name="ApiName",
            hostname="api.hostname",
            port=1234,
            response_buffer_size=1024,
            timeout=5,
            ssl=False,
            enums={},
            structs={
                "SomeStruct": StructModel(
                    name="SomeStruct",
                    fields=[
                        StructFieldModel(name="SomeField2", type="int"),
                        StructFieldModel(name="SomeField1", type="str", default_value="'some default string value'"),
                        StructFieldModel(name="SomeField3", type="float", default_value="3.14"),
                    ]
                ),
                "AnotherStruct": StructModel(
                    name="AnotherStruct",
                    fields=[
                        StructFieldModel(name="AnotherField1", type="str"),
                        StructFieldModel(name="AnotherField3", type="float"),
                        StructFieldModel(name="AnotherField2", type="int", default_value="12"),
                    ]
                )
            },
            commands=[]
        )

        output: ApiModel = ApiModelCreator().create(api_spec)

        self.assertEqual(output, expected_model)

    def test_create_structs_only_with_list_to_primitive_type(self):
        api_spec: dict = {
            "api_name": "ApiName",
            "hostname": "api.hostname",
            "port": 1234,
            "response_buffer_size": 1024,
            "timeout": 5,
            "ssl": False,
            "enums": {},
            "structs": {
                "SomeStruct": {
                    "SomeField1": "str",
                    "SomeField2": "List[int]",
                    "SomeField3": "float",
                },
                "AnotherStruct": {
                    "AnotherField1": "str",
                    "AnotherField2": "int",
                    "AnotherField3": "List[float]",
                }
            },
            "commands": {},
        }

        expected_model: ApiModel = ApiModel(
            name="ApiName",
            hostname="api.hostname",
            port=1234,
            response_buffer_size=1024,
            timeout=5,
            ssl=False,
            enums={},
            structs={
                "SomeStruct": StructModel(
                    name="SomeStruct",
                    fields=[
                        StructFieldModel(name="SomeField1", type="str"),
                        StructFieldModel(name="SomeField2", type="List[int]"),
                        StructFieldModel(name="SomeField3", type="float"),
                    ],
                    dependencies={
                        "List": ListModel()
                    }
                ),
                "AnotherStruct": StructModel(
                    name="AnotherStruct",
                    fields=[
                        StructFieldModel(name="AnotherField1", type="str"),
                        StructFieldModel(name="AnotherField2", type="int"),
                        StructFieldModel(name="AnotherField3", type="List[float]"),
                    ],
                    dependencies={
                        "List": ListModel()
                    }
                )
            },
            commands=[]
        )

        output: ApiModel = ApiModelCreator().create(api_spec)

        self.assertEqual(output, expected_model)

    def test_create_structs_only_with_list_to_enum_type(self):
        api_spec: dict = {
            "api_name": "ApiName",
            "hostname": "api.hostname",
            "port": 1234,
            "response_buffer_size": 1024,
            "timeout": 5,
            "ssl": False,
            "enums": {
                "SomeEnum": {
                    "SomeEnumField1": "0",
                    "SomeEnumField2": "1",
                    "SomeEnumField3": "2",
                },
            },
            "structs": {
                "SomeStruct": {
                    "SomeField1": "str",
                    "SomeField2": "List[SomeEnum]",
                    "SomeField3": "float",
                },
            },
            "commands": {},
        }

        expected_model: ApiModel = ApiModel(
            name="ApiName",
            hostname="api.hostname",
            port=1234,
            response_buffer_size=1024,
            timeout=5,
            ssl=False,
            enums={
                "SomeEnum": EnumModel(
                    name="SomeEnum",
                    fields=[
                        EnumFieldModel(name="SomeEnumField1", value="0"),
                        EnumFieldModel(name="SomeEnumField2", value="1"),
                        EnumFieldModel(name="SomeEnumField3", value="2"),
                    ]
                ),
            },
            structs={
                "SomeStruct": StructModel(
                    name="SomeStruct",
                    fields=[
                        StructFieldModel(name="SomeField1", type="str"),
                        StructFieldModel(name="SomeField2", type="List[SomeEnum]"),
                        StructFieldModel(name="SomeField3", type="float"),
                    ],
                    dependencies={
                        "SomeEnum": EnumModel(
                            name="SomeEnum",
                            fields=[
                                EnumFieldModel(name="SomeEnumField1", value="0"),
                                EnumFieldModel(name="SomeEnumField2", value="1"),
                                EnumFieldModel(name="SomeEnumField3", value="2"),
                            ]
                        ),
                        "List": ListModel()
                    }
                )
            },
            commands=[]
        )

        output: ApiModel = ApiModelCreator().create(api_spec)

        self.assertEqual(output, expected_model)

    def test_create_structs_with_enum_dependency(self):
        api_spec: dict = {
            "api_name": "ApiName",
            "hostname": "api.hostname",
            "port": 1234,
            "response_buffer_size": 1024,
            "timeout": 5,
            "ssl": False,
            "enums": {
                "SomeEnum": {
                    "SomeEnumField1": "0",
                    "SomeEnumField2": "1",
                },
            },
            "structs": {
                "SomeStruct": {
                    "SomeField1": "str",
                    "SomeField2": "SomeEnum",
                },
            },
            "commands": {},
        }

        expected_model: ApiModel = ApiModel(
            name="ApiName",
            hostname="api.hostname",
            port=1234,
            response_buffer_size=1024,
            timeout=5,
            ssl=False,
            enums={
                "SomeEnum": EnumModel(
                    name="SomeEnum",
                    fields=[
                        EnumFieldModel(name="SomeEnumField1", value="0"),
                        EnumFieldModel(name="SomeEnumField2", value="1"),
                    ]
                ),
            },
            structs={
                "SomeStruct": StructModel(
                    name="SomeStruct",
                    fields=[
                        StructFieldModel(name="SomeField1", type="str"),
                        StructFieldModel(name="SomeField2", type="SomeEnum"),
                    ],
                    dependencies={
                        "SomeEnum": EnumModel(
                            name="SomeEnum",
                            fields=[
                                EnumFieldModel(name="SomeEnumField1", value="0"),
                                EnumFieldModel(name="SomeEnumField2", value="1"),
                            ]
                        ),
                    }
                )
            },
            commands=[]
        )

        output: ApiModel = ApiModelCreator().create(api_spec)

        self.assertEqual(output, expected_model)

    def test_create_structs_with_struct_dependency(self):
        api_spec: dict = {
            "api_name": "ApiName",
            "hostname": "api.hostname",
            "port": 1234,
            "response_buffer_size": 1024,
            "timeout": 5,
            "ssl": False,
            "enums": {},
            "structs": {
                "SomeStruct": {
                    "SomeField1": "str",
                    "SomeField2": "AnotherStruct",
                },
                "AnotherStruct": {
                    "AnotherField1": "int",
                    "AnotherField2": "float",
                }
            },
            "commands": {},
        }

        another_struct_model: StructModel = StructModel(
            name="AnotherStruct",
            fields=[
                StructFieldModel(name="AnotherField1", type="int"),
                StructFieldModel(name="AnotherField2", type="float"),
            ]
        )
        expected_model: ApiModel = ApiModel(
            name="ApiName",
            hostname="api.hostname",
            port=1234,
            response_buffer_size=1024,
            timeout=5,
            ssl=False,
            enums={},
            structs={
                "SomeStruct": StructModel(
                    name="SomeStruct",
                    fields=[
                        StructFieldModel(name="SomeField1", type="str"),
                        StructFieldModel(name="SomeField2", type="AnotherStruct"),
                    ],
                    dependencies={
                        "AnotherStruct": another_struct_model
                    }
                ),
                "AnotherStruct": another_struct_model
            },
            commands=[]
        )

        output: ApiModel = ApiModelCreator().create(api_spec)

        self.assertEqual(output, expected_model)

    def test_create_commands(self):
        api_spec: dict = {
            "api_name": "ApiName",
            "hostname": "api.hostname",
            "port": 1234,
            "response_buffer_size": 1024,
            "timeout": 5,
            "ssl": False,
            "enums": {},
            "structs": {},
            "commands": {
                "SomeCommand": {
                    "request": {
                        "SomeField1": "str",
                        "SomeField2": "int",
                    },
                    "response": {
                        "SomeField3": "float",
                        "SomeField4": "str",
                    },
                    "silent": True,
                },
                "AnotherCommand": {
                    "request": {
                        "AnotherField1": "float",
                        "AnotherField2": "str",
                    },
                    "response": {
                        "AnotherField3": "str",
                        "AnotherField4": "int",
                    },
                    "silent": False,
                }
            },
        }

        expected_model: ApiModel = ApiModel(
            name="ApiName",
            hostname="api.hostname",
            port=1234,
            response_buffer_size=1024,
            timeout=5,
            ssl=False,
            enums={},
            structs={
                "SomeCommandRequest": StructModel(
                    name="SomeCommandRequest",
                    fields=[
                        StructFieldModel(name="SomeField1", type="str"),
                        StructFieldModel(name="SomeField2", type="int"),
                    ]
                ),
                "SomeCommandResponse": StructModel(
                    name="SomeCommandResponse",
                    fields=[
                        StructFieldModel(name="SomeField3", type="float"),
                        StructFieldModel(name="SomeField4", type="str"),
                    ]
                ),
                "AnotherCommandRequest": StructModel(
                    name="AnotherCommandRequest",
                    fields=[
                        StructFieldModel(name="AnotherField1", type="float"),
                        StructFieldModel(name="AnotherField2", type="str"),
                    ]
                ),
                "AnotherCommandResponse": StructModel(
                    name="AnotherCommandResponse",
                    fields=[
                        StructFieldModel(name="AnotherField3", type="str"),
                        StructFieldModel(name="AnotherField4", type="int"),
                    ]
                )
            },
            commands=[
                CommandModel(
                    name="SomeCommand",
                    request=StructModel(
                        name="SomeCommandRequest",
                        fields=[
                            StructFieldModel(name="SomeField1", type="str"),
                            StructFieldModel(name="SomeField2", type="int"),
                        ]
                    ),
                    response=StructModel(
                        name="SomeCommandResponse",
                        fields=[
                            StructFieldModel(name="SomeField3", type="float"),
                            StructFieldModel(name="SomeField4", type="str"),
                        ]
                    ),
                    silent=True,
                ),
                CommandModel(
                    name="AnotherCommand",
                    request=StructModel(
                        name="AnotherCommandRequest",
                        fields=[
                            StructFieldModel(name="AnotherField1", type="float"),
                            StructFieldModel(name="AnotherField2", type="str"),
                        ]
                    ),
                    response=StructModel(
                        name="AnotherCommandResponse",
                        fields=[
                            StructFieldModel(name="AnotherField3", type="str"),
                            StructFieldModel(name="AnotherField4", type="int"),
                        ]
                    ),
                    silent=False
                )
            ]
        )

        output: ApiModel = ApiModelCreator().create(api_spec)

        self.assertEqual(output, expected_model)
