import socket
import threading

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

    # Specify the path to the HTML file
    html_file_path = "index.html"  # Assuming the HTML file is named index.html and is in the same directory

    # Read the content of the HTML file
    with open(html_file_path, "rb") as file:
        response_body = file.read()

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

    try:
        while True:
            print(f"Server listening on http://{SERVER_ADDRESS[0]}:{SERVER_ADDRESS[1]}")
            print("Waiting for a connection...")
            conn, addr = server_socket.accept()
            print(f"Connection from {addr}")

            # Handle the client request in a new thread
            client_thread = threading.Thread(target=handle_request, args=(conn, addr))
            client_thread.start()

    except KeyboardInterrupt:
        print("Server stopped")
        server_socket.close()


if __name__ == "__main__":
    start_server()
