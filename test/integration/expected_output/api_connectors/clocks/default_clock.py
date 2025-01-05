import time

from .clock_interface import ClockInterface
from ..types import Timestamp, PreciseTimestamp


class DefaultClock(ClockInterface):
    def get_time(self) -> Timestamp:
        return int(time.time())

    def get_precise_time(self) -> PreciseTimestamp:
        return int(time.time() * 1000)