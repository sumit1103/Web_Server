import socket
import mimetypes

host = "127.0.0.1"
port = 64534

response_template = """\
HTTP/1.1 {rstatus_code}
Content-Type: {content_type}
Content-Length: {content_length}
Connecton: close

"""

def read_file(file_path):
    try:
        print(f"Trying to open file: {file_path}")
        with open(file_path,'rb') as f: #rb is neccesary while dealing with non textual files such as image, pdf
            file_content = f.read()
            print()
            print(f"File content read successfully, length: {len(file_content)}")
            return file_content, "200 OK"
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return "<html><head></head><body>404 file not found</body></html>", "404 Not FOUND"
    except IsADirectoryError:
        print(f"Attempted directory access: {file_path}")
        return "<html><head></head><body>403 Forbidden: Directory access is not allowed</body></html>", "403 FORBIDDEN"


def get_mime_type(filepath):  #used to determine the MIME type (also known as the "media type" or "content type") of a file based on its file extension.
    mime_type, _ = mimetypes.guess_type(filepath) #returns a tuple (mime_type, encoding)
    return mime_type or "application/octet-stream"


try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((host, port))
        s.listen(2)
        s.settimeout(10)
        print()
        print("Waiting for the connection........")
        print()

        while True:
            conn, addr = s.accept()
            with conn:
                try:
                    data = conn.recv(1024 * 50).decode('utf-8')  # Decode byte data to string
                    if not data:
                        print("Empty request received") 
                        raise ValueError("Empty request received")
                    
                    print(f"Received Request: {data}")

                    if not data.startswith("GET") or "HTTP/1.1" not in data:
                        raise ValueError("Malformed HTTP request")
                    
                    requested_file = data.split()[1]
                    if requested_file == '/':
                        requested_file = '/Login.html'

                    filepath = f'./html_files{requested_file}'
                    html_content, response_code = read_file(filepath)
                    if isinstance(html_content, str):
                        html_content = html_content.encode('utf-8')  # Convert to bytes if it's a string
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
                    try:
                        conn.sendall(error_message.encode('utf-8'))
                    except BrokenPipeError:
                        print("Client closed the connection before receiving the response.")

                except Exception as e:  # Catch any unexpected errors for 500 status code
                    error_message = f"<html><head></head><body>500 Internal Server Error: {str(e)}</body></html>"
                    html_content = error_message.encode('utf-8')
                    response = response_template.format(
                        rstatus_code="500 Internal Server Error",
                        content_type="text/html",
                        content_length=len(html_content)
                    ).encode('utf-8')

                    conn.sendall(response)
                    conn.sendall(html_content)

                finally:
                    conn.close()

except KeyboardInterrupt:
    print("\nServer stopped by user")