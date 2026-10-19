import socket

HOST = "127.0.0.1"
PORT = 8081

MAX_HEADER_SIZE = 8192
TIMEOUT = 5


def read_request(connection):
    data = b""

    while b"\r\n\r\n" not in data:
        chunk = connection.recv(4096)

        if not chunk:
            raise ValueError("Incomplete HTTP request")

        data += chunk

        header_end = data.find(b"\r\n\r\n")

        if header_end == -1 and len(data) > MAX_HEADER_SIZE:
            raise ValueError("Headers too large")

        if header_end > MAX_HEADER_SIZE:
            raise ValueError("Headers too large")

    return data[:header_end + 4]


def parse_request(data):
    text = data.decode("iso-8859-1")
    lines = text.split("\r\n")

    parts = lines[0].split(" ")

    if len(parts) != 3 or not all(parts):
        raise ValueError("Invalid request line")

    method, path, version = parts

    if version != "HTTP/1.1":
        raise ValueError("Unsupported HTTP version")

    if not path.startswith("/"):
        raise ValueError("Invalid request path")

    headers = {}

    for line in lines[1:]:
        if not line:
            break

        if ":" not in line:
            raise ValueError("Invalid header")

        name, value = line.split(":", 1)
        name = name.strip().lower()

        if not name:
            raise ValueError("Invalid header name")

        headers[name] = value.strip()

    if "host" not in headers:
        raise ValueError("Missing Host header")

    return method, path, version, headers


def create_response(status, body):
    body = body.encode("utf-8")

    reasons = {
        200: "OK",
        400: "Bad Request",
        405: "Method Not Allowed",
        408: "Request Timeout",
        431: "Request Header Fields Too Large",
    }

    reason = reasons[status]

    return (
        f"HTTP/1.1 {status} {reason}\r\n"
        "Content-Type: text/plain; charset=utf-8\r\n"
        f"Content-Length: {len(body)}\r\n"
        "Connection: close\r\n"
        "\r\n"
    ).encode("ascii") + body


def handle_connection(connection):
    connection.settimeout(TIMEOUT)

    try:
        data = read_request(connection)
        method, path, version, headers = parse_request(data)

        print(f"Method:  {method}")
        print(f"Path:    {path}")
        print(f"Version: {version}")
        print(f"Headers: {headers}")

        if method != "GET":
            response = create_response(405, "Method Not Allowed")
        else:
            body = (
                f"Method: {method}\n"
                f"Path: {path}\n"
                f"Version: {version}\n"
                f"Headers: {headers}\n"
            )
            response = create_response(200, body)

    except socket.timeout:
        response = create_response(408, "Request Timeout")

    except ValueError as error:
        print(f"Bad request: {error}")

        if str(error) == "Headers too large":
            response = create_response(431, "Headers Too Large")
        else:
            response = create_response(400, "Bad Request")

    connection.sendall(response)


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((HOST, PORT))
        server.listen(5)

        print(f"Server running at http://{HOST}:{PORT}")

        while True:
            connection, address = server.accept()

            with connection:
                print(f"\nConnected by {address}")

                try:
                    handle_connection(connection)
                except OSError as error:
                    print(f"Connection error: {error}")


if __name__ == "__main__":
    main()