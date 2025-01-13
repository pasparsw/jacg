from abc import abstractmethod

from ..types import DecodedRequest, DecodedResponse, Milliseconds


class ApiConnectorInterface:
    @abstractmethod
    def connect(self, hostname: str, port: int, response_buffer_size: int, response_timeout: Milliseconds,
                socket_timeout: Milliseconds, min_pause_between_requests: Milliseconds) -> None:
        pass

    @abstractmethod
    def send(self, request: DecodedRequest) -> DecodedResponse:
        pass
