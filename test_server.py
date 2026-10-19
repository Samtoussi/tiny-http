import unittest

from server import parse_request, create_response


class TestHTTPServer(unittest.TestCase):

    def test_valid_request(self):
        request = (
            b"GET /hello HTTP/1.1\r\n"
            b"Host: localhost\r\n"
            b"\r\n"
        )

        method, path, version, headers = parse_request(request)

        self.assertEqual(method, "GET")
        self.assertEqual(path, "/hello")
        self.assertEqual(version, "HTTP/1.1")
        self.assertEqual(headers["host"], "localhost")

    def test_missing_host(self):
        request = b"GET / HTTP/1.1\r\n\r\n"

        with self.assertRaises(ValueError):
            parse_request(request)

    def test_invalid_request_line(self):
        request = b"INVALID\r\nHost: localhost\r\n\r\n"

        with self.assertRaises(ValueError):
            parse_request(request)

    def test_valid_response(self):
        response = create_response(200, "Hello")

        self.assertIn(b"HTTP/1.1 200 OK", response)
        self.assertIn(b"Content-Length: 5", response)
        self.assertTrue(response.endswith(b"Hello"))

    def test_error_response(self):
        response = create_response(400, "Bad Request")

        self.assertIn(b"HTTP/1.1 400 Bad Request", response)


if __name__ == "__main__":
    unittest.main()