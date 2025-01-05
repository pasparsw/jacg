from abc import abstractmethod

from ..types import Seconds, DecodedRequest, DecodedResponse


class ApiConnectorInterface:
    @abstractmethod
    def connect(self, hostname: str, port: int, response_buffer_size: int, response_timeout: Seconds,
                socket_timeout: Seconds) -> None:
        pass

    @abstractmethod
    def send(self, request: DecodedRequest) -> DecodedResponse:
        pass
