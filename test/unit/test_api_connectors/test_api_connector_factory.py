import unittest

from src.api_connectors.api_connector_factory import ApiConnectorFactory
from src.api_connectors.api_connector_type import ApiConnectorType
from src.api_connectors.clocks.default_clock import DefaultClock
from src.api_connectors.connectors.api_connector_interface import ApiConnectorInterface
from src.api_connectors.connectors.default_api_connector import DefaultApiConnector
from src.api_connectors.json_encoders.default_json_encoder import DefaultJsonEncoder
from src.api_connectors.sockets.default_socket import DefaultSocket
from src.api_connectors.sockets.ssl_socket import SslSocket


class TestApiConnectorFactory(unittest.TestCase):
    def test_create_returns_object_of_proper_type(self):
        default_connector: ApiConnectorInterface = ApiConnectorFactory.create(ApiConnectorType.DEFAULT)
        ssl_connector: ApiConnectorInterface = ApiConnectorFactory.create(ApiConnectorType.SSL)

        self.assertTrue(isinstance(default_connector, DefaultApiConnector))
        self.assertTrue(isinstance(ssl_connector, DefaultApiConnector))

        self.assertTrue(isinstance(default_connector.socket, DefaultSocket))
        self.assertTrue(isinstance(default_connector.json_encoder, DefaultJsonEncoder))
        self.assertTrue(isinstance(default_connector.clock, DefaultClock))

        self.assertTrue(isinstance(ssl_connector.socket, SslSocket))
        self.assertTrue(isinstance(ssl_connector.json_encoder, DefaultJsonEncoder))
        self.assertTrue(isinstance(ssl_connector.clock, DefaultClock))
