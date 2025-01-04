from abc import abstractmethod

from src.api_connectors.types import Seconds, DecodedRequest, DecodedResponse


class ApiConnectorInterface:
    @abstractmethod
    def connect(self, hostname: str, port: int, response_buffer_size: int, timeout: Seconds) -> None:
        pass

    @abstractmethod
    def send(self, request: DecodedRequest) -> DecodedResponse:
        pass
