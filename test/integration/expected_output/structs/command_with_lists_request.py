from dataclasses import dataclass

from typing import List


@dataclass
class CommandWithListsRequest:
    arg: List[str]
