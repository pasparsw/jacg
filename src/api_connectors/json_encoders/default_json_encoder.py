import json

from logging import getLogger

from src.api_connectors.json_encoders.json_decoding_failed import JsonDecodingFailed
from src.api_connectors.json_encoders.json_encoder_interface import JsonEncoderInterface

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
            LOGGER.debug(f"Decoding {len(encoded_json)} bytes to JSON")

            decoded_json, size = self.__decoder.raw_decode(encoded_json.decode())

            LOGGER.debug(f"Decoded JSON of size {size}")

            return decoded_json
        except json.decoder.JSONDecodeError as e:
            LOGGER.error(e)
            raise JsonDecodingFailed()
