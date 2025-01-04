import unittest
from unittest.mock import MagicMock, Mock, call

from src.json_socket_handler.exceptions.communication_timeout import CommunicationTimeout
from src.json_socket_handler.ssl.ssl_json_socket_handler import SslJsonSocketHandler
from src.json_socket_handler.types import Seconds


class TestSslJsonSocketHandler(unittest.TestCase):
    def test_connect_calls_proper_commands(self):
        sock = MagicMock(connect=Mock())
        json_encoder = MagicMock()
        clock = MagicMock()
        hostname: str = "some.hostname.com"
        port: int = 1234
        response_buffer_size: int = 1024
        timeout: Seconds = 10

        uut = SslJsonSocketHandler(sock, json_encoder, clock)

        uut.connect(hostname, port, response_buffer_size, timeout)

        sock.connect.assert_called_once_with(hostname, port, timeout)

    def test_successful_send_calls_proper_commands_for_small_request_and_small_response(self):
        sock = MagicMock(connect=Mock(), send=Mock(), receive=Mock())
        json_encoder = MagicMock(encode=Mock())
        clock = MagicMock(get_time=Mock())
        hostname: str = "some.hostname.com"
        port: int = 1234
        response_buffer_size: int = 1024
        timeout: Seconds = 10
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

        clock.get_time.side_effect = [0, 1, 2, 3]
        json_encoder.encode.return_value = encoded_request
        sock.send.return_value = len(encoded_request)
        sock.receive.side_effect = [encoded_response, b""]
        json_encoder.decode.return_value = expected_response

        uut = SslJsonSocketHandler(sock, json_encoder, clock)

        uut.connect(hostname, port, response_buffer_size, timeout)
        response: dict = uut.send(request)

        sock.connect.assert_called_once_with(hostname, port, timeout)

        json_encoder.encode.assert_called_once_with(request)
        sock.send.assert_called_once_with(encoded_request)
        sock.receive.assert_has_calls([
            call(response_buffer_size),
            call(response_buffer_size),
        ])
        json_encoder.decode.assert_called_once_with(encoded_response)

        self.assertEqual(clock.get_time.call_count, 4)
        self.assertEqual(response, expected_response)

    def test_successful_send_calls_proper_commands_for_multi_chunk_request_and_small_response(self):
        sock = MagicMock(connect=Mock(), send=Mock(), receive=Mock())
        json_encoder = MagicMock(encode=Mock())
        clock = MagicMock(get_time=Mock())
        hostname: str = "some.hostname.com"
        port: int = 1234
        response_buffer_size: int = 1024
        timeout: Seconds = 10
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

        clock.get_time.side_effect = [0, 1, 2, 3, 4, 5]
        json_encoder.encode.return_value = encoded_request
        sock.send.side_effect = [6, 4, 5]
        sock.receive.side_effect = [encoded_response, b""]
        json_encoder.decode.return_value = expected_response

        uut = SslJsonSocketHandler(sock, json_encoder, clock)

        uut.connect(hostname, port, response_buffer_size, timeout)
        response: dict = uut.send(request)

        sock.connect.assert_called_once_with(hostname, port, timeout)

        json_encoder.encode.assert_called_once_with(request)
        sock.send.assert_has_calls([
            call(encoded_request),
            call(encoded_request[6:]),
            call(encoded_request[10:]),
        ])
        sock.receive.assert_has_calls([
            call(response_buffer_size),
            call(response_buffer_size)
        ])
        json_encoder.decode.assert_called_once_with(encoded_response)

        self.assertEqual(clock.get_time.call_count, 6)
        self.assertEqual(response, expected_response)

    def test_successful_send_calls_proper_commands_for_small_request_and_multi_chunk_response(self):
        sock = MagicMock(connect=Mock(), send=Mock(), receive=Mock())
        json_encoder = MagicMock(encode=Mock())
        clock = MagicMock(get_time=Mock())
        hostname: str = "some.hostname.com"
        port: int = 1234
        response_buffer_size: int = 1024
        timeout: Seconds = 10
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

        clock.get_time.side_effect = [0, 1, 2, 3, 4, 5]
        json_encoder.encode.return_value = encoded_request
        sock.send.return_value = len(encoded_request)
        sock.receive.side_effect = [
            encoded_response[:6],
            encoded_response[6:10],
            encoded_response[10:],
            b""]
        json_encoder.decode.return_value = expected_response

        uut = SslJsonSocketHandler(sock, json_encoder, clock)

        uut.connect(hostname, port, response_buffer_size, timeout)
        response: dict = uut.send(request)

        sock.connect.assert_called_once_with(hostname, port, timeout)

        json_encoder.encode.assert_called_once_with(request)
        sock.send.assert_called_once_with(encoded_request)
        sock.receive.assert_has_calls([
            call(response_buffer_size),
            call(response_buffer_size),
            call(response_buffer_size),
            call(response_buffer_size),
        ])
        json_encoder.decode.assert_called_once_with(encoded_response)

        self.assertEqual(clock.get_time.call_count, 6)
        self.assertEqual(response, expected_response)

    def test_successful_send_calls_proper_commands_for_multi_chunk_request_and_multi_chunk_response(self):
        sock = MagicMock(connect=Mock(), send=Mock(), receive=Mock())
        json_encoder = MagicMock(encode=Mock())
        clock = MagicMock(get_time=Mock())
        hostname: str = "some.hostname.com"
        port: int = 1234
        response_buffer_size: int = 1024
        timeout: Seconds = 10
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

        clock.get_time.side_effect = [0, 1, 2, 3, 4, 5, 6, 7]
        json_encoder.encode.return_value = encoded_request
        sock.send.side_effect = [6, 4, 5]
        sock.receive.side_effect = [
            encoded_response[:6],
            encoded_response[6:10],
            encoded_response[10:],
            b""]
        json_encoder.decode.return_value = expected_response

        uut = SslJsonSocketHandler(sock, json_encoder, clock)

        uut.connect(hostname, port, response_buffer_size, timeout)
        response: dict = uut.send(request)

        sock.connect.assert_called_once_with(hostname, port, timeout)

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
            call(response_buffer_size),
        ])
        json_encoder.decode.assert_called_once_with(encoded_response)

        self.assertEqual(clock.get_time.call_count, 8)
        self.assertEqual(response, expected_response)

    def test_send_raises_proper_exception_when_send_timeout(self):
        sock = MagicMock(connect=Mock(), send=Mock(), receive=Mock())
        json_encoder = MagicMock(encode=Mock())
        clock = MagicMock(get_time=Mock())
        hostname: str = "some.hostname.com"
        port: int = 1234
        response_buffer_size: int = 1024
        timeout: Seconds = 10
        request: dict = {
            "arg_1": "value_1",
            "arg_2": "value_2",
        }
        encoded_request: bytes = b"encoded_request"

        clock.get_time.side_effect = [0, 1, 2, 11]
        json_encoder.encode.return_value = encoded_request
        sock.send.side_effect = [6, 4, 5]

        uut = SslJsonSocketHandler(sock, json_encoder, clock)

        uut.connect(hostname, port, response_buffer_size, timeout)
        with self.assertRaises(CommunicationTimeout):
            uut.send(request)

        sock.connect.assert_called_once_with(hostname, port, timeout)

        json_encoder.encode.assert_called_once_with(request)
        sock.send.assert_has_calls([
            call(encoded_request),
            call(encoded_request[6:]),
        ])

        self.assertEqual(clock.get_time.call_count, 4)

    def test_send_raises_proper_exception_when_receive_timeout(self):
        sock = MagicMock(connect=Mock(), send=Mock(), receive=Mock())
        json_encoder = MagicMock(encode=Mock())
        clock = MagicMock(get_time=Mock())
        hostname: str = "some.hostname.com"
        port: int = 1234
        response_buffer_size: int = 1024
        timeout: Seconds = 10
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

        clock.get_time.side_effect = [0, 1, 2, 3, 11]
        json_encoder.encode.return_value = encoded_request
        sock.send.return_value = len(encoded_request)
        sock.receive.side_effect = [
            encoded_response[:6],
            encoded_response[6:10],
            encoded_response[10:],
            b""]
        json_encoder.decode.return_value = expected_response

        uut = SslJsonSocketHandler(sock, json_encoder, clock)

        uut.connect(hostname, port, response_buffer_size, timeout)

        with self.assertRaises(CommunicationTimeout):
            uut.send(request)

        sock.connect.assert_called_once_with(hostname, port, timeout)

        json_encoder.encode.assert_called_once_with(request)
        sock.send.assert_called_once_with(encoded_request)
        sock.receive.assert_has_calls([
            call(response_buffer_size),
            call(response_buffer_size),
        ])

        self.assertEqual(clock.get_time.call_count, 5)
