import socket

from logging import getLogger

from .socket_interface import SocketInterface
from ..types import Milliseconds

LOGGER = getLogger("DefaultSocket")


class DefaultSocket(SocketInterface):
    def __init__(self):
        self.__socket = None

    def connect(self, hostname: str, port: int, timeout: Milliseconds) -> None:
        LOGGER.debug(f"Connecting to {hostname}:{port} with timeout {timeout}")

        self.__socket = socket.create_connection((hostname, port))
        self.__socket.settimeout(timeout)

        LOGGER.debug(f"Socket connected")

    def send(self, data: bytes) -> int:
        LOGGER.debug(f"Sending {len(data)} bytes")
        return self.__socket.send(data)

    def receive(self, buffer_size: int) -> bytes:
        try:
            return self.__socket.recv(buffer_size)
        except TimeoutError as e:
            LOGGER.warning(f"{e} - returning empty byte string")
            return b""
