from abc import abstractmethod

from api_connectors.types import Seconds


class SocketInterface:
    @abstractmethod
    def connect(self, hostname: str, port: int, timeout: Seconds) -> None:
        pass

    @abstractmethod
    def send(self, data: bytes) -> int:
        pass

    @abstractmethod
    def receive(self, buffer_size: int) -> bytes:
        pass
