from abc import abstractmethod


class SslContextInterface:
    @abstractmethod
    def wrap_socket(self, socket: SocketInterface, hostname: str) -> SocketInterface:
        pass
