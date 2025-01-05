from logging import getLogger

from src.api_connectors.clocks.clock_interface import ClockInterface
from src.api_connectors.connectors.communication_timeout import CommunicationTimeout
from src.api_connectors.json_encoders.json_decoding_failed import JsonDecodingFailed
from src.api_connectors.json_encoders.json_encoder_interface import JsonEncoderInterface
from src.api_connectors.connectors.api_connector_interface import ApiConnectorInterface, Seconds
from src.api_connectors.sockets.socket_interface import SocketInterface
from src.api_connectors.types import DecodedRequest, DecodedResponse, Timestamp, PreciseTimestamp

LOGGER = getLogger("DefaultApiConnector")


class DefaultApiConnector(ApiConnectorInterface):
    def __init__(self, sock: SocketInterface, json_encoder: JsonEncoderInterface, clock: ClockInterface):
        self.__socket: SocketInterface = sock
        self.__json_encoder: JsonEncoderInterface = json_encoder
        self.__clock: ClockInterface = clock
        self.__response_buffer_size: int = 0
        self.__timeout: Seconds = 0

    @property
    def socket(self) -> SocketInterface:
        return self.__socket

    @property
    def json_encoder(self) -> JsonEncoderInterface:
        return self.__json_encoder

    @property
    def clock(self) -> ClockInterface:
        return self.__clock

    def connect(self, hostname: str, port: int, response_buffer_size: int, response_timeout: Seconds,
                socket_timeout: Seconds) -> None:
        LOGGER.debug(f"Connecting default API connector to {hostname}:{port} with buffer size {response_buffer_size}, "
                     f"response timeout {response_timeout}s and socket timeout {socket_timeout}")

        self.__socket.connect(hostname, port, socket_timeout)
        self.__response_buffer_size = response_buffer_size
        self.__timeout = response_timeout

        LOGGER.debug(f"Default API connector connected")

    def send(self, request: DecodedRequest) -> DecodedResponse:
        LOGGER.debug(f"Sending request")

        start_timestamp: Timestamp = self.__clock.get_time()
        encoded_request: bytes = self.__json_encoder.encode(request)
        total_data_sent: int = 0
        send_iterations: int = 0
        send_start_timestamp: PreciseTimestamp = self.__clock.get_precise_time()

        while total_data_sent < len(encoded_request):
            self.__check_timeout(start_timestamp, "Failed to send JSON request!")

            send_iterations += 1
            data_sent: int = self.__socket.send(encoded_request[total_data_sent:])
            total_data_sent += data_sent

            LOGGER.debug(f"Sent {data_sent} out of {len(encoded_request)} request bytes")

        send_elapsed_time: PreciseTimestamp = self.__clock.get_precise_time() - send_start_timestamp
        LOGGER.debug(f"Sent {total_data_sent} bytes in {send_elapsed_time}ms after {send_iterations} iterations")

        encoded_response: bytes = b""
        response_ready: bool = False
        decoded_response: DecodedResponse = {}
        receive_iterations: int = 0
        receive_start_timestamp: PreciseTimestamp = self.__clock.get_precise_time()

        while not response_ready:
            self.__check_timeout(start_timestamp, "Failed to receive JSON response!")

            receive_iterations += 1
            received_data: bytes = self.__socket.receive(self.__response_buffer_size)
            encoded_response += received_data
            response_ready = len(received_data) < self.__response_buffer_size

            LOGGER.debug(f"Received {len(received_data)} response bytes")

            if response_ready:
                try:
                    decoded_response = self.__json_encoder.decode(encoded_response)
                    response_ready = True
                except JsonDecodingFailed as _:
                    LOGGER.debug("Response not ready yet - listening for further data...")
                    response_ready = False

        receive_elapsed_time: PreciseTimestamp = self.__clock.get_precise_time() - receive_start_timestamp
        LOGGER.debug(f"Complete response received ({len(encoded_response)} bytes) in {receive_elapsed_time}ms after "
                     f"{receive_iterations} iterations")

        return decoded_response

    def __check_timeout(self, start_timestamp: Timestamp, error_message: str) -> None:
        if self.__clock.get_time() - start_timestamp > self.__timeout:
            raise CommunicationTimeout(error_message)
