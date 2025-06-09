import socket

host = "127.0.0.1"
port = 64534

file_name = "/Login.html"
request_template ="""
GET {file} HTTP/3.0
Host: localhost
Content-Type: application/pdf

"""

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as c:
    print()
    print("Trying to make connection with server")
    print()
    try:
        c.connect((host, port))
        request = request_template.format(
            file=file_name
        )

        c.sendall(request.encode('utf-8'))  # Send request to the server

        # Receive the response from the server as binary data
        data = b""
        while True:
            packet = c.recv(4096)
            if not packet:
                break
            data += packet
        # Print the received binary data directly to the terminal
        print(f"Received binary data, length: {len(data)} bytes")
        print(data.decode('utf-8'))  # Print the binary content directly

    except ConnectionRefusedError:
        print()
        print("Connection refused")
        print()
