import socket

host = "127.0.0.1"
port = 64534

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as c:
    print()
    print("Trying to make connection with server")
    print()
    try:
        c.connect((host, port))

        # Send an empty request to the server (trigger the Empty request received error)
        c.sendall(b"")  # Sending an empty byte string

        # Receive the response from the server
        data = b""
        while True:
            packet = c.recv(4096)
            if not packet:
                break
            data += packet

        # Print the received response from the server
        print(f"Received response, length: {len(data)} bytes")
        print(data.decode('utf-8'))  # Decode and print the server's response

    except ConnectionRefusedError:
        print()
        print("Connection refused")
        print()
