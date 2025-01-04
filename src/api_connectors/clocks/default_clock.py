import time

from src.api_connectors.clocks.clock_interface import ClockInterface
from src.api_connectors.types import Timestamp


class DefaultClock(ClockInterface):
    def get_time(self) -> Timestamp:
        return int(time.time())
