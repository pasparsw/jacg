import time

from .clock_interface import ClockInterface
from ..types import PreciseTimestamp, Milliseconds


class DefaultClock(ClockInterface):
    def get_precise_time(self) -> PreciseTimestamp:
        return int(time.time() * 1000)

    def sleep(self, duration: Milliseconds) -> None:
        time.sleep(duration/1000)
