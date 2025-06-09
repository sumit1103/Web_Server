import socket
import select
import mimetypes

host = "127.0.0.1"
port = 64534

response_template = """\
HTTP/1.1 {rstatus_code}
Content-Type: {content_type}
Content-Length: {content_length}
Connection: close

"""

def read_file(file_path):
    try:
        with open(file_path, 'rb') as f:
            return f.read(), "200 OK"
    except FileNotFoundError:
        return "<html><head></head><body>404 file not found</body></html>", "404 Not Found"
    except IsADirectoryError:
        return "<html><head></head><body>403 Forbidden: Directory access is not allowed</body></html>", "403 Forbidden"

def get_mime_type(filepath):
    mime_type, _ = mimetypes.guess_type(filepath)
    return mime_type or "application/octet-stream"

def handle_request(conn):
    try:
        data = conn.recv(1024 * 50).decode('utf-8')  # Decode byte data to string
        if not data:
            raise ValueError("Empty request received")
        
        if not data.startswith("GET") or "HTTP/1.1" not in data:
            raise ValueError("Malformed HTTP request")
        
        requested_file = data.split()[1]
        if requested_file == '/':
            requested_file = '/Login.html'

        filepath = f'./html_files{requested_file}'
        html_content, response_code = read_file(filepath)
        if isinstance(html_content, str):
            html_content = html_content.encode('utf-8')
        content_type = get_mime_type(filepath)

        response = response_template.format(
            rstatus_code=response_code,
            content_type=content_type,
            content_length=len(html_content)
        ).encode('utf-8')

        conn.sendall(response)
        conn.sendall(html_content)

    except ValueError as e:
        error_message = f"<html><head></head><body>400 Bad Request: {str(e)}</body></html>"
        html_content = error_message.encode('utf-8')
        response = response_template.format(
            rstatus_code="400 Bad Request",
            content_type="text/html",
            content_length=len(html_content)
        ).encode('utf-8')

        conn.sendall(response)
        conn.sendall(html_content)

    except Exception as e:
        error_message = f"<html><head></head><body>500 Internal Server Error: {str(e)}</body></html>"
        html_content = error_message.encode('utf-8')
        response = response_template.format(
            rstatus_code="500 Internal Server Error",
            content_type="text/html",
            content_length=len(html_content)
        ).encode('utf-8')

        conn.sendall(response)
        conn.sendall(html_content)

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    server_socket.listen(5)
    server_socket.setblocking(False)

    inputs = [server_socket]  # List of sockets to monitor
    print("Waiting for connections...")

    while True:
        readable, writable, exceptional = select.select(inputs, [], inputs)
        
        for s in readable:
            if s is server_socket:
                # Handle new connections
                conn, addr = s.accept()
                print(f"Connected to {addr}")
                conn.setblocking(False)
                inputs.append(conn)
            else:
                # Handle existing connections
                try:
                    handle_request(s)
                except Exception as e:
                    print(f"Error handling request: {e}")
                finally:
                    s.close()
                    inputs.remove(s)

        for s in exceptional:
            inputs.remove(s)
            s.close()

if __name__ == "__main__":
    main()
