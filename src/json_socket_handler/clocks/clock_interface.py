from abc import abstractmethod

from src.json_socket_handler.types import Timestamp


class ClockInterface:
    @abstractmethod
    def get_time(self) -> Timestamp:
        pass
