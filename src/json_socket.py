import ssl
import socket
import json
import time

from logging import getLogger

LOGGER = getLogger("JsonSocket")


class RequestFailed(Exception):
    pass


class JsonSocket:
    def __init__(self, hostname: str, port: int, response_buffer_size: int, timeout_s: int, use_ssl: bool):
        LOGGER.info(f"Creating JSON socket for {hostname}:{port} with buffer size {response_buffer_size}")

        self.__context = ssl.create_default_context()
        self.__sock = socket.create_connection((hostname, port))
        self.__json_decoder = json.JSONDecoder()
        self.__response_buffer_size: int = response_buffer_size
        self.__timeout: int = timeout_s
        
        if use_ssl:
            self.__sock = self.__context.wrap_socket(self.__sock, server_hostname=hostname)

        LOGGER.info(f"JSON socket created")

    def send(self, request: dict) -> dict:
        request_string: str = json.dumps(request)
        encoded_request: bytes = request_string.encode("utf-8")

        self.__sock.send(encoded_request)

        received_data: str = ""
        decoded_response: dict = {}
        start_timestamp: float = time.time()

        while True:
            if time.time() - start_timestamp > self.__timeout:
                raise RequestFailed("Failed to send request - timeout!")

            received_data += self.__sock.recv(self.__response_buffer_size).decode()

            try:
                (decoded_response, size) = self.__json_decoder.raw_decode(received_data)

                if size == len(received_data):
                    break
                elif size < len(received_data):
                    received_data = received_data[size:].strip()
                    break
            except ValueError as e:
                LOGGER.info(f"Error during response decoding: {e}")
                continue

        return decoded_response
