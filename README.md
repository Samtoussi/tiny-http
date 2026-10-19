# Tiny-HTTP

A minimal HTTP/1.1 server built from scratch using Python's
standard library.

## Features

- TCP socket server
- Basic HTTP request parsing
- HTTP header parsing
- HTTP status codes (200, 400, 405, 408, 431)
- Request timeouts
- Header size limits
- Automated unit tests

## Run

python3 server.py

## Tests

python3 -m unittest discover -v

## Roadmap

- [x] V1 - TCP server and basic HTTP responses
- [x] V2 - HTTP parsing and error handling
- [ ] V3 - Routing and responses
- [ ] V4 - Multiple clients
- [ ] V5 - Final testing and release