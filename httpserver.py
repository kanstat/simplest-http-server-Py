import socket

# Define the server address and port
SERVER_ADDRESS = ("localhost", 8000)

# Define the allowed origins for CORS
ALLOWED_ORIGINS = [
    "http://localhost:8000",
    "null",
]  # Allow requests from file:// URLs and the same origin


def handle_request(conn, addr):
    # Receive the HTTP request
    request_data = conn.recv(1024)
    print("Received request:", request_data.decode())  # For debugging

    # Construct the response body as a byte object
    response_body = b"<html><body><h1>Hello, World!</h1></body></html>"
    content_length = len(response_body)

    # Construct the response headers with CORS
    response_headers = [
        "HTTP/1.1 200 OK",
        "Content-Type: text/html",
        f"Content-Length: {content_length}",
        "Connection: close",
        "Access-Control-Allow-Origin: *",  # Allow all origins for simplicity
        "Access-Control-Allow-Methods: GET, POST, OPTIONS",
        "Access-Control-Allow-Headers: Content-Type",
    ]

    # Combine headers into a single string, add a blank line to separate headers from the body
    response_header_str = "\r\n".join(response_headers) + "\r\n\r\n"

    # Send the combined response
    conn.sendall(response_header_str.encode() + response_body)
    conn.close()


def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(SERVER_ADDRESS)
    server_socket.listen(1)
    print(f"Server listening on {SERVER_ADDRESS[0]}:{SERVER_ADDRESS[1]}")

    try:
        while True:
            print("Waiting for a connection...")
            conn, addr = server_socket.accept()
            print(f"Connection from {addr}")

            # Handle the client request
            handle_request(conn, addr)

    except KeyboardInterrupt:
        print("Server stopped")
        server_socket.close()


if __name__ == "__main__":
    start_server()
