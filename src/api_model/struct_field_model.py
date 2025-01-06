class StructFieldModel:
    def __init__(self, name: str, type: str, default_value: any = None):
        self.name: str = name
        self.type: str = type
        self.default_value: any = default_value

    def __eq__(self, other) -> bool:
        return self.name == other.name and self.type == other.type and self.default_value == other.default_value

    def __str__(self) -> str:
        return f"(name: {self.name}, type: {self.type}, default_value: {self.default_value})"

    @property
    def underlying_type(self) -> str:
        if self.is_list():
            return self.type[self.type.find("[") + 1:self.type.find("]")]
        return self.type

    @property
    def non_mutable_default_value(self) -> any:
        if self.is_list() and self.has_default_value() and self.default_value == "[]":
            return "field(default_factory=lambda: [])"
        return self.default_value

    def is_list(self) -> bool:
        return "[" in self.type and "]" in self.type

    def has_default_value(self) -> bool:
        return self.default_value is not None

    def default_value_empty(self):
        if self.default_value:
            return self.default_value == "[]" or self.default_value == "{}"
        return True
