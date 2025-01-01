from dataclasses import dataclass

from typing import List


@dataclass
class CommandWithListsResponse:
    returned_value: List[int]
