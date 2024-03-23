import os
import socket
import threading

# Define the server address and port
SERVER_ADDRESS = ("localhost", 8000)

# Define the allowed origins for CORS
ALLOWED_ORIGINS = [
    "http://localhost:8000",
    "null",
]  # Allow requests from file:// URLs and the same origin

STATUS_CODE = {
    200: "HTTP/1.1 200 OK",
    201: "HTTP/1.1 201 Created",
    204: "HTTP/1.1 204 No Content",
    301: "HTTP/1.1 301 Moved Permanently",
    302: "HTTP/1.1 302 Found",
    400: "HTTP/1.1 400 Bad Request",
    401: "HTTP/1.1 401 Unauthorized",
    403: "HTTP/1.1 403 Forbidden",
    404: "HTTP/1.1 404 Not Found",
    405: "HTTP/1.1 405 Method Not Allowed",
    500: "HTTP/1.1 500 Internal Server Error",
    503: "HTTP/1.1 503 Service Unavailable",
}

# Base directory is the current folder where this script is located
BASE_DIR = os.path.dirname(os.path.realpath(__file__))


def handle_request(conn, addr):
    try:
        # Receive the HTTP request
        request_data = conn.recv(1024).decode()
        if not request_data:
            conn.close()
            return
        print("Received request:", request_data[0:14], "  ....")  # For debugging

        # Parse the first line of the request to get the method and path
        request_line = request_data.splitlines()[0]
        method, path, _ = request_line.split()

        # Default path to index.html if root is requested
        if path == "/":
            path = "/index.html"

        # Construct the file path
        file_path = os.path.join(BASE_DIR, path.strip("/"))

        # Check if the file exists and is not a directory
        if os.path.exists(file_path) and not os.path.isdir(file_path):
            with open(file_path, "rb") as file:
                response_body = file.read()
            status_code = f"{STATUS_CODE[200]}"
            # Determine content type
            if file_path.endswith(".css"):
                content_type = "text/css"
            elif file_path.endswith(".js"):
                content_type = "application/javascript"
            elif file_path.endswith(".html"):
                content_type = "text/html"
        else:
            # File not found, send 404 response
            response_body = b"<h1>404 Not Found</h1>"
            content_type = "text/html"
            status_code = f"{STATUS_CODE[404]}"

        content_length = len(response_body)

        # Construct the response headers with CORS
        response_headers = [
            f"{status_code}",
            f"Content-Type: {content_type}",
            f"Content-Length: {content_length}",
            "Connection: close",
            "Access-Control-Allow-Origin: *",  # Allow all origins for simplicity
            "Access-Control-Allow-Methods: GET, POST, OPTIONS",
            "Access-Control-Allow-Headers: Content-Type",
        ]

        # Combine headers into a single string, add a blank line to separate headers from the body
        response_header_str = "\r\n".join(response_headers) + "\r\n\r\n"

        print(f"Response: {status_code}\n")
        # Send the combined response
        conn.sendall(response_header_str.encode() + response_body)
        conn.close()
    except:
        print("\n************ EXCEPTION ***********\n")
        response_body = b"<h1>404 Not Found</h1>"
        content_length = len(response_body)
        content_type = "text/html"
        response_headers = [
            "HTTP/1.1 404 Not Found",
            f"Content-Type: {content_type}",
            f"Content-Length: {content_length}",
            "Connection: close",
            "Access-Control-Allow-Origin: *",  # Allow all origins for simplicity
            "Access-Control-Allow-Methods: GET, POST, OPTIONS",
            "Access-Control-Allow-Headers: Content-Type",
        ]
        conn.sendall(response_header_str.encode() + response_body)
        conn.close()


def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(SERVER_ADDRESS)
    server_socket.listen(5)
    print(f"Server listening on http://{SERVER_ADDRESS[0]}:{SERVER_ADDRESS[1]}")
    server_socket.settimeout(1)

    try:
        print("Waiting for a connection...")
        while True:
            try:
                conn, addr = server_socket.accept()
                print(f"Connection from {addr}")

                # Handle the client request in a new thread
                client_thread = threading.Thread(
                    target=handle_request, args=(conn, addr), name=f"{addr[1]}"
                )
                client_thread.start()
            except socket.timeout:
                pass
            except KeyboardInterrupt:
                try:
                    if conn:
                        conn.close()
                except:
                    pass
                break
    except KeyboardInterrupt:
        print("Server stopped")
        server_socket.close()


if __name__ == "__main__":
    start_server()
