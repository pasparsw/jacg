from logging import getLogger

from src.json_socket_handler.clocks.clock_interface import ClockInterface
from src.json_socket_handler.exceptions.communication_timeout import CommunicationTimeout
from src.json_socket_handler.json_decoders.json_encoder_interface import JsonEncoderInterface
from src.json_socket_handler.json_socket_handler_interface import JsonSocketHandlerInterface, Seconds
from src.json_socket_handler.sockets.socket_interface import SocketInterface
from src.json_socket_handler.types import DecodedRequest, DecodedResponse, Timestamp

LOGGER = getLogger("JsonSocket")


class SslJsonSocketHandler(JsonSocketHandlerInterface):
    def __init__(self, sock: SocketInterface, json_encoder: JsonEncoderInterface, clock: ClockInterface):
        LOGGER.debug(f"Creating SSL JSON socket handler")

        self.__socket: SocketInterface = sock
        self.__json_encoder: JsonEncoderInterface = json_encoder
        self.__clock: ClockInterface = clock
        self.__response_buffer_size: int = 0
        self.__timeout: Seconds = 0

        LOGGER.debug(f"SSL JSON socket handler created")

    def connect(self, hostname: str, port: int, response_buffer_size: int, timeout: Seconds) -> None:
        LOGGER.debug(f"Connecting JSON socket for {hostname}:{port} with buffer size {response_buffer_size} and timeout "
                     f"{timeout}")

        self.__socket.connect(hostname, port, timeout)
        self.__response_buffer_size = response_buffer_size
        self.__timeout = timeout

        LOGGER.debug(f"Successfully connected to {hostname}:{port}!")

    def send(self, request: DecodedRequest) -> DecodedResponse:
        start_timestamp: Timestamp = self.__clock.get_time()
        encoded_request: bytes = self.__json_encoder.encode(request)
        total_data_sent: int = 0

        while total_data_sent < len(encoded_request):
            self.__check_timeout(start_timestamp, "Failed to send JSON request!")

            data_sent: int = self.__socket.send(encoded_request[total_data_sent:])
            total_data_sent += data_sent

        encoded_response: bytes = b""
        response_ready: bool = False

        while not response_ready:
            self.__check_timeout(start_timestamp, "Failed to receive JSON response!")

            received_data: bytes = self.__socket.receive(self.__response_buffer_size)
            encoded_response += received_data
            response_ready = received_data == b""

        return self.__json_encoder.decode(encoded_response)

    def __check_timeout(self, start_timestamp: Timestamp, error_message: str) -> None:
        if self.__clock.get_time() - start_timestamp > self.__timeout:
            raise CommunicationTimeout(error_message)
