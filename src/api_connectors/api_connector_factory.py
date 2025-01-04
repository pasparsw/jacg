from src.api_connectors.clocks.clock_interface import ClockInterface
from src.api_connectors.clocks.default_clock import DefaultClock
from src.api_connectors.json_encoders.default_json_encoder import DefaultJsonEncoder
from src.api_connectors.json_encoders.json_encoder_interface import JsonEncoderInterface
from src.api_connectors.connectors.api_connector_interface import ApiConnectorInterface
from src.api_connectors.api_connector_type import ApiConnectorType
from src.api_connectors.sockets.default_socket import DefaultSocket
from src.api_connectors.sockets.socket_interface import SocketInterface
from src.api_connectors.sockets.ssl_socket import SslSocket
from src.api_connectors.connectors.default_api_connector import DefaultApiConnector


class UnsupportedJsonSocketHandlerType(Exception):
    pass


class ApiConnectorFactory:
    @staticmethod
    def create(connector_type: ApiConnectorType) -> ApiConnectorInterface:
        if connector_type == ApiConnectorType.DEFAULT:
            return ApiConnectorFactory.__create_default_connector()
        if connector_type == ApiConnectorType.SSL:
            return ApiConnectorFactory.__create_ssl_connector()

        raise UnsupportedJsonSocketHandlerType(f"Unsupported JSON socket handler type: {connector_type}")

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
