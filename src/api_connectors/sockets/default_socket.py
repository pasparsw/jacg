import socket

from logging import getLogger

from src.api_connectors.sockets.socket_interface import SocketInterface
from src.api_connectors.types import Seconds

LOGGER = getLogger("DefaultSocket")


class DefaultSocket(SocketInterface):
    def __init__(self):
        self.__socket = None

    def connect(self, hostname: str, port: int, timeout: Seconds) -> None:
        LOGGER.debug(f"Connecting to {hostname}:{port} with timeout {timeout}")

        self.__socket = socket.create_connection((hostname, port))
        self.__socket.settimeout(timeout)

        LOGGER.debug(f"Socket connected")

    def send(self, data: bytes) -> int:
        LOGGER.debug(f"Sending {len(data)} bytes")
        return self.__socket.send(data)

    def receive(self, buffer_size: int) -> bytes:
        LOGGER.debug(f"Receiving buffer of {buffer_size} bytes")
        return self.__socket.recv(buffer_size)
