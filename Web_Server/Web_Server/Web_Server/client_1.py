import socket
import mimetypes

host = "127.0.0.1"
port = 64534

file_name = "/Login.html"
request_template = """
GET {file} HTTP/1.1
Host: localhost
Content-Type: {content_type}
Connection: close

"""
def get_mime_type():
    mime_types, _ = mimetypes.guess_type(file_name)
    return mime_types or "application/octet-stream"

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as c:
    print("Trying to make connection with server")
    try:
        c.connect((host, port))
        content_type = get_mime_type()
        request = request_template.format(
            file=file_name,
            content_type = content_type
            ).encode('utf-8')
        c.sendall(request)

        # Receive data in chunks
        data = b""
        while True:
            packet = c.recv(4096)
            if not packet:
                break
            data += packet
        print()
        print(f"Received data:\n\n {data.decode('utf-8')}")
    except ConnectionRefusedError:
        print("Connection refused")
    finally:
        c.close()
