from abc import abstractmethod

from src.api_connectors.types import Timestamp, PreciseTimestamp


class ClockInterface:
    @abstractmethod
    def get_time(self) -> Timestamp:
        pass

    @abstractmethod
    def get_precise_time(self) -> PreciseTimestamp:
        pass
