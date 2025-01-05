from .clocks.clock_interface import ClockInterface
from .clocks.default_clock import DefaultClock
from .json_encoders.default_json_encoder import DefaultJsonEncoder
from .json_encoders.json_encoder_interface import JsonEncoderInterface
from .connectors.api_connector_interface import ApiConnectorInterface
from .api_connector_type import ApiConnectorType
from .sockets.default_socket import DefaultSocket
from .sockets.socket_interface import SocketInterface
from .sockets.ssl_socket import SslSocket
from .connectors.default_api_connector import DefaultApiConnector


class UnsupportedJsonSocketHandlerType(Exception):
    pass


class ApiConnectorFactory:
    @staticmethod
    def create(connector_type: ApiConnectorType) -> ApiConnectorInterface:
        if connector_type == ApiConnectorType.DEFAULT:
            return ApiConnectorFactory.__create_default_connector()
        if connector_type == ApiConnectorType.SSL:
            return ApiConnectorFactory.__create_ssl_connector()

        raise UnsupportedJsonSocketHandlerType(f"Unsupported API connector type: {connector_type}")

    @staticmethod
    def __create_default_connector() -> ApiConnectorInterface:
        sock: SocketInterface = DefaultSocket()
        json_encoder: JsonEncoderInterface = DefaultJsonEncoder()
        clock: ClockInterface = DefaultClock()

        return DefaultApiConnector(sock, json_encoder, clock)

    @staticmethod
    def __create_ssl_connector() -> ApiConnectorInterface:
        sock: SocketInterface = SslSocket()
        json_encoder: JsonEncoderInterface = DefaultJsonEncoder()
        clock: ClockInterface = DefaultClock()

        return DefaultApiConnector(sock, json_encoder, clock)
