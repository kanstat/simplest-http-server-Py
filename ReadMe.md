***Note:** Just for learning purposes, not intended or safe to be used for real web applications.*

# Simple HTTP Server in Python

This repository contains a basic implementation of an HTTP server using Python's socket programming. The server is just capable of handling HTTP GET requests and responding with a simple HTML page. Additionally, it includes basic CORS (Cross-Origin Resource Sharing) support to allow requests from different origins.

## Features

- **HTTP GET Request Handling:** The server processes HTTP GET requests and returns a predefined HTML response, including CSS and JavaScript files.
- **Interactive Web Page:** Includes a simple interactive web page with a click counter, demonstrating how to serve static files (HTML, CSS, JavaScript) and handle user interactions.
- **CORS Support:** Implements basic CORS headers to allow cross-origin requests.
- **Connection Handling:** Manages client connections, receiving requests, and sending responses using Python's low-level socket API.


## Getting Started

### Prerequisites

- Python 3.x installed on your machine.

### Running the Server

1. Windows OS
  

```powershell
python httpserver.py
```

2. Linux or Mac
  

```bash
python3 httpserver.py
```
