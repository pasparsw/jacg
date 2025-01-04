from abc import abstractmethod


class JsonEncoderInterface:
    @abstractmethod
    def encode(self, decoded_json: dict) -> bytes:
        pass

    @abstractmethod
    def decode(self, encoded_json: bytes) -> dict:
        pass
