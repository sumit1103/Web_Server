import socket
import mimetypes

host = "127.0.0.1"
port = 64534

response_template = """\
HTTP/1.1 {rstatus_code}
Content-Type: {content_type}
Content-Length: {content_length}

"""

def read_file(file_path):
    try:
        with open(file_path, 'rb') as f:  # Read in binary mode
            return f.read(), "200 OK"
    except FileNotFoundError:
        return b"<html><head></head><body>404 file not found</body></html>", "404 NOT FOUND"
    except IsADirectoryError:
        return b"<html><head></head><body>403 Forbidden: Directory access is not allowed</body></html>", "403 FORBIDDEN"

def get_mime_type(filepath):
    mime_type, _ = mimetypes.guess_type(filepath)
    return mime_type or "application/octet-stream"

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((host, port))
    s.listen(2)
    print("\nWaiting for the connection...\n")

    while True:
        conn, addr = s.accept()
        with conn:
            print(f'Connected to {addr}')
            data = conn.recv(1024).decode('utf-8')

            if data:
                print("\nReceived Request:\n", data)
                requested_file = data.split()[1]

                if requested_file == '/':
                    requested_file = '/Login.html'  # Default to Login.html for root requests

                filepath = f'./html_files{requested_file}'
                file_content, response_code = read_file(filepath)
                content_type = get_mime_type(filepath)

                # Build the HTTP response header
                response_headers = response_template.format(
                    rstatus_code=response_code,
                    content_type=content_type,
                    content_length=len(file_content)
                ).encode('utf-8')

                # Send headers first, then content
                conn.sendall(response_headers)
                conn.sendall(file_content)  # Send content (text or binary)
