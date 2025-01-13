from abc import abstractmethod

from ..types import Milliseconds


class SocketInterface:
    @abstractmethod
    def connect(self, hostname: str, port: int, timeout: Milliseconds) -> None:
        pass

    @abstractmethod
    def send(self, data: bytes) -> int:
        pass

    @abstractmethod
    def receive(self, buffer_size: int) -> bytes:
        pass
