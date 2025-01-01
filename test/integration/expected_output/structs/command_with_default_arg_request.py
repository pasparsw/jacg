from dataclasses import dataclass



@dataclass
class CommandWithDefaultArgRequest:
    arg_2: float
    arg_1: str = 'default_value'
    arg_3: int = 5
