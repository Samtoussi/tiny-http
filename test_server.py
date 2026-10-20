import unittest

from server import parse_request, create_response, route_request


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

    def test_query_parameters(self):
        request = (
            b"GET /hello?name=Sam HTTP/1.1\r\n"
            b"Host: localhost\r\n"
            b"\r\n"
        )

        method, path, version, headers = parse_request(request)

        self.assertEqual(path, "/hello")

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

    def test_root_route(self):
        status, body = route_request("GET", "/")

        self.assertEqual(status, 200)
        self.assertEqual(body, "Welcome to Tiny-HTTP!")

    def test_hello_route(self):
        status, body = route_request("GET", "/hello")

        self.assertEqual(status, 200)
        self.assertEqual(body, "Hello, World!")

    def test_health_route(self):
        status, body = route_request("GET", "/health")

        self.assertEqual(status, 200)
        self.assertEqual(body, "OK")

    def test_unknown_route(self):
        status, body = route_request("GET", "/unknown")

        self.assertEqual(status, 404)
        self.assertEqual(body, "404 Not Found")

    def test_unsupported_method(self):
        status, body = route_request("POST", "/hello")

        self.assertEqual(status, 405)
        self.assertEqual(body, "Method Not Allowed")

    def test_not_found_response(self):
        response = create_response(404, "404 Not Found")

        self.assertIn(b"HTTP/1.1 404 Not Found", response)


if __name__ == "__main__":
    unittest.main()