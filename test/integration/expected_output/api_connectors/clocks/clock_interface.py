from abc import abstractmethod

from ..types import PreciseTimestamp, Milliseconds


class ClockInterface:
    @abstractmethod
    def get_precise_time(self) -> PreciseTimestamp:
        pass

    @abstractmethod
    def sleep(self, duration: Milliseconds) -> None:
        pass
