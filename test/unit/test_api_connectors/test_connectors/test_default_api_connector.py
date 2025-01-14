import unittest

from unittest.mock import MagicMock, Mock, call

from src.exceptions.communication_timeout import CommunicationTimeout
from src.api_connectors.connectors.default_api_connector import DefaultApiConnector
from src.api_connectors.types import Milliseconds


class TestDefaultApiConnector(unittest.TestCase):
    def test_connect_calls_proper_commands(self):
        sock = MagicMock(connect=Mock())
        json_encoder = MagicMock()
        clock = MagicMock(get_precise_time=Mock())
        hostname: str = "some.hostname.com"
        port: int = 1234
        response_buffer_size: int = 1024
        response_timeout: Milliseconds = 10000
        socket_timeout: Milliseconds = 3000

        clock.get_precise_time.side_effect = [0, 1, 2]

        uut = DefaultApiConnector(sock, json_encoder, clock)

        uut.connect(hostname, port, response_buffer_size, response_timeout, socket_timeout, min_pause_between_requests=0)

        sock.connect.assert_called_once_with(hostname, port, socket_timeout)

        self.assertEqual(clock.get_precise_time.call_count, 3)

    def test_successful_send_calls_proper_commands_for_small_request_and_small_response(self):
        sock = MagicMock(connect=Mock(), send=Mock(), receive=Mock())
        json_encoder = MagicMock(encode=Mock())
        clock = MagicMock(get_precise_time=Mock())
        hostname: str = "some.hostname.com"
        port: int = 1234
        response_buffer_size: int = 1024
        response_timeout: Milliseconds = 10000
        socket_timeout: Milliseconds = 3000
        request: dict = {
            "arg_1": "value_1",
            "arg_2": "value_2",
        }
        encoded_request: bytes = b"encoded_request"
        encoded_response: bytes = b"encoded_response"
        expected_response: dict = {
            "arg_3": "value_3",
            "arg_4": "value_4",
        }

        clock.get_precise_time.side_effect = [0, 1000, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000]
        json_encoder.encode.return_value = encoded_request
        sock.send.return_value = len(encoded_request)
        sock.receive.return_value = encoded_response
        json_encoder.decode.return_value = expected_response

        uut = DefaultApiConnector(sock, json_encoder, clock)

        uut.connect(hostname, port, response_buffer_size, response_timeout, socket_timeout, min_pause_between_requests=0)
        response: dict = uut.send(request)

        sock.connect.assert_called_once_with(hostname, port, socket_timeout)

        json_encoder.encode.assert_called_once_with(request)
        sock.send.assert_called_once_with(encoded_request)
        sock.receive.assert_called_once_with(response_buffer_size)
        json_encoder.decode.assert_called_once_with(encoded_response)

        self.assertEqual(clock.get_precise_time.call_count, 12)
        self.assertEqual(response, expected_response)
    #
    def test_successful_send_calls_proper_commands_for_multi_chunk_request_and_small_response(self):
        sock = MagicMock(connect=Mock(), send=Mock(), receive=Mock())
        json_encoder = MagicMock(encode=Mock())
        clock = MagicMock(get_precise_time=Mock())
        hostname: str = "some.hostname.com"
        port: int = 1234
        response_buffer_size: int = 1024
        response_timeout: Milliseconds = 10000
        socket_timeout: Milliseconds = 3000
        request: dict = {
            "arg_1": "value_1",
            "arg_2": "value_2",
        }
        encoded_request: bytes = b"encoded_request"
        encoded_response: bytes = b"encoded_response"
        expected_response: dict = {
            "arg_3": "value_3",
            "arg_4": "value_4",
        }

        clock.get_precise_time.side_effect = [0, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 11000, 12000,
                                              13000, 14000]
        json_encoder.encode.return_value = encoded_request
        sock.send.side_effect = [6, 4, 5]
        sock.receive.side_effect = [encoded_response, b""]
        json_encoder.decode.return_value = expected_response

        uut = DefaultApiConnector(sock, json_encoder, clock)

        uut.connect(hostname, port, response_buffer_size, response_timeout, socket_timeout, min_pause_between_requests=0)
        response: dict = uut.send(request)

        sock.connect.assert_called_once_with(hostname, port, socket_timeout)

        json_encoder.encode.assert_called_once_with(request)
        sock.send.assert_has_calls([
            call(encoded_request),
            call(encoded_request[6:]),
            call(encoded_request[10:]),
        ])
        sock.receive.assert_called_once_with(response_buffer_size)
        json_encoder.decode.assert_called_once_with(encoded_response)

        self.assertEqual(clock.get_precise_time.call_count, 14)
        self.assertEqual(response, expected_response)

    def test_successful_send_calls_proper_commands_for_small_request_and_multi_chunk_response(self):
        sock = MagicMock(connect=Mock(), send=Mock(), receive=Mock())
        json_encoder = MagicMock(encode=Mock())
        clock = MagicMock(get_precise_time=Mock())
        hostname: str = "some.hostname.com"
        port: int = 1234
        response_buffer_size: int = 6
        response_timeout: Milliseconds = 10000
        socket_timeout: Milliseconds = 3000
        request: dict = {
            "arg_1": "value_1",
            "arg_2": "value_2",
        }
        encoded_request: bytes = b"encoded_request"
        encoded_response: bytes = b"encoded_response"
        expected_response: dict = {
            "arg_3": "value_3",
            "arg_4": "value_4",
        }

        clock.get_precise_time.side_effect = [0, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 11000, 12000,
                                              13000, 14000]
        json_encoder.encode.return_value = encoded_request
        sock.send.return_value = len(encoded_request)
        sock.receive.side_effect = [
            encoded_response[:6],
            encoded_response[6:12],
            encoded_response[12:]
        ]
        json_encoder.decode.return_value = expected_response

        uut = DefaultApiConnector(sock, json_encoder, clock)

        uut.connect(hostname, port, response_buffer_size, response_timeout, socket_timeout, min_pause_between_requests=0)
        response: dict = uut.send(request)

        sock.connect.assert_called_once_with(hostname, port, socket_timeout)

        json_encoder.encode.assert_called_once_with(request)
        sock.send.assert_called_once_with(encoded_request)
        sock.receive.assert_has_calls([
            call(response_buffer_size),
            call(response_buffer_size),
            call(response_buffer_size),
        ])
        json_encoder.decode.assert_called_once_with(encoded_response)

        self.assertEqual(clock.get_precise_time.call_count, 14)
        self.assertEqual(response, expected_response)

    def test_successful_send_calls_proper_commands_for_multi_chunk_request_and_multi_chunk_response(self):
        sock = MagicMock(connect=Mock(), send=Mock(), receive=Mock())
        json_encoder = MagicMock(encode=Mock())
        clock = MagicMock(get_precise_time=Mock())
        hostname: str = "some.hostname.com"
        port: int = 1234
        response_buffer_size: int = 6
        response_timeout: Milliseconds = 10000
        socket_timeout: Milliseconds = 3000
        request: dict = {
            "arg_1": "value_1",
            "arg_2": "value_2",
        }
        encoded_request: bytes = b"encoded_request"
        encoded_response: bytes = b"encoded_response"
        expected_response: dict = {
            "arg_3": "value_3",
            "arg_4": "value_4",
        }

        clock.get_precise_time.side_effect = [0, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 11000, 12000,
                                              13000, 14000, 15000, 16000, 17000]
        json_encoder.encode.return_value = encoded_request
        sock.send.side_effect = [6, 4, 5]
        sock.receive.side_effect = [
            encoded_response[:6],
            encoded_response[6:12],
            encoded_response[12:],
        ]
        json_encoder.decode.return_value = expected_response

        uut = DefaultApiConnector(sock, json_encoder, clock)

        uut.connect(hostname, port, response_buffer_size, response_timeout, socket_timeout, min_pause_between_requests=0)
        response: dict = uut.send(request)

        sock.connect.assert_called_once_with(hostname, port, socket_timeout)

        json_encoder.encode.assert_called_once_with(request)
        sock.send.assert_has_calls([
            call(encoded_request),
            call(encoded_request[6:]),
            call(encoded_request[10:]),
        ])
        sock.receive.assert_has_calls([
            call(response_buffer_size),
            call(response_buffer_size),
            call(response_buffer_size),
        ])
        json_encoder.decode.assert_called_once_with(encoded_response)

        self.assertEqual(clock.get_precise_time.call_count, 16)
        self.assertEqual(response, expected_response)

    def test_send_raises_proper_exception_when_send_timeout(self):
        sock = MagicMock(connect=Mock(), send=Mock(), receive=Mock())
        json_encoder = MagicMock(encode=Mock())
        clock = MagicMock(get_precise_time=Mock())
        hostname: str = "some.hostname.com"
        port: int = 1234
        response_buffer_size: int = 1024
        response_timeout: Milliseconds = 10000
        socket_timeout: Milliseconds = 3000
        request: dict = {
            "arg_1": "value_1",
            "arg_2": "value_2",
        }
        encoded_request: bytes = b"encoded_request"

        clock.get_precise_time.side_effect = [0, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 19000]
        json_encoder.encode.return_value = encoded_request
        sock.send.side_effect = [6, 4, 5]

        uut = DefaultApiConnector(sock, json_encoder, clock)

        uut.connect(hostname, port, response_buffer_size, response_timeout, socket_timeout, min_pause_between_requests=0)
        with self.assertRaises(CommunicationTimeout):
            uut.send(request)

        sock.connect.assert_called_once_with(hostname, port, socket_timeout)

        json_encoder.encode.assert_called_once_with(request)
        sock.send.assert_has_calls([
            call(encoded_request),
            call(encoded_request[6:]),
        ])

        self.assertEqual(clock.get_precise_time.call_count, 10)

    def test_send_raises_proper_exception_when_receive_timeout(self):
        sock = MagicMock(connect=Mock(), send=Mock(), receive=Mock())
        json_encoder = MagicMock(encode=Mock())
        clock = MagicMock(get_precise_time=Mock())
        hostname: str = "some.hostname.com"
        port: int = 1234
        response_buffer_size: int = 6
        response_timeout: Milliseconds = 10000
        socket_timeout: Milliseconds = 3000
        request: dict = {
            "arg_1": "value_1",
            "arg_2": "value_2",
        }
        encoded_request: bytes = b"encoded_request"
        encoded_response: bytes = b"encoded_response"
        expected_response: dict = {
            "arg_3": "value_3",
            "arg_4": "value_4",
        }

        clock.get_precise_time.side_effect = [0, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000, 11000,
                                              22000]
        json_encoder.encode.return_value = encoded_request
        sock.send.return_value = len(encoded_request)
        sock.receive.side_effect = [
            encoded_response[:6],
            encoded_response[6:12],
            encoded_response[12:],
        ]
        json_encoder.decode.return_value = expected_response

        uut = DefaultApiConnector(sock, json_encoder, clock)

        uut.connect(hostname, port, response_buffer_size, response_timeout, socket_timeout, min_pause_between_requests=0)

        with self.assertRaises(CommunicationTimeout):
            uut.send(request)

        sock.connect.assert_called_once_with(hostname, port, socket_timeout)

        json_encoder.encode.assert_called_once_with(request)
        sock.send.assert_called_once_with(encoded_request)
        sock.receive.assert_has_calls([
            call(response_buffer_size),
            call(response_buffer_size),
        ])

        self.assertEqual(clock.get_precise_time.call_count, 13)
