from abc import abstractmethod

from src.api_connectors.types import Timestamp


class ClockInterface:
    @abstractmethod
    def get_time(self) -> Timestamp:
        pass
