from abc import abstractmethod

from src.json_socket_handler.types import Seconds, DecodedRequest, DecodedResponse


class JsonSocketHandlerInterface:
    @abstractmethod
    def connect(self, hostname: str, port: int, response_buffer_size: int, timeout: Seconds) -> None:
        pass

    @abstractmethod
    def send(self, request: DecodedRequest) -> DecodedResponse:
        pass
