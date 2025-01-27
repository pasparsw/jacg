import json

from logging import getLogger

from ...exceptions.json_decoding_failed import JsonDecodingFailed
from .json_encoder_interface import JsonEncoderInterface

LOGGER = getLogger("DefaultJsonEncoder")


class DefaultJsonEncoder(JsonEncoderInterface):
    def __init__(self):
        self.__decoder = json.JSONDecoder()

    def encode(self, decoded_json: dict) -> bytes:
        LOGGER.debug("Encoding JSON object to UTF-8")

        json_string: str = json.dumps(decoded_json)
        return json_string.encode("utf-8")

    def decode(self, encoded_json: bytes) -> dict:
        try:
            decoded_json, size = self.__decoder.raw_decode(encoded_json.decode())

            LOGGER.debug(f"Decoded JSON of size {size}")

            return decoded_json
        except json.decoder.JSONDecodeError as _:
            raise JsonDecodingFailed()
