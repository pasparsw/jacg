import socket
import ssl

from logging import getLogger, exception

from .socket_interface import SocketInterface
from ..types import Seconds

LOGGER = getLogger("SslSocket")


class SslSocket(SocketInterface):
    def __init__(self):
        self.__socket = None

    def connect(self, hostname: str, port: int, timeout: Seconds) -> None:
        LOGGER.debug(f"Connecting to {hostname}:{port} with timeout {timeout}")

        self.__socket = socket.create_connection((hostname, port))
        self.__socket.settimeout(timeout)

        ssl_context = ssl.create_default_context()
        self.__socket = ssl_context.wrap_socket(self.__socket, server_hostname=hostname)

        LOGGER.debug(f"Socket connected")

    def send(self, data: bytes) -> int:
        LOGGER.debug(f"Sending {len(data)} bytes")
        return self.__socket.send(data)

    def receive(self, buffer_size: int) -> bytes:
        try:
            LOGGER.debug(f"Receiving buffer of {buffer_size} bytes")
            return self.__socket.recv(buffer_size)
        except TimeoutError as e:
            LOGGER.warning(f"{e} - returning empty byte string")
            return b""
