# 🌐 Custom Web Server Using Python

This project implements a custom web server and multiple clients in Python. It simulates basic HTTP interactions, error handling, and serves static HTML content. It serves as a foundational demonstration of socket programming, request handling, and web technologies.

## 🎯 Project Objectives

- Build a basic HTTP server from scratch using sockets  
- Simulate client-server communication through Python clients  
- Serve static HTML content using custom logic  
- Handle HTTP methods and errors manually (e.g., 404, empty request)  
- Explore low-level networking concepts in a web context  

## 🛠️ Technologies Used

- **Language:** Python (Sockets, Threading)  
- **Frontend:** HTML  
- **Server/Backend:** Custom Python-based server  
- **Tools:** Socket programming, basic HTTP protocol emulation  

## 💡 Key Features

- Multi-client support using threads  
- Handles custom HTTP GET requests  
- Serves static HTML files from a directory  
- Logs request and response activities  
- Graceful handling of empty or malformed requests  
- Extendable architecture for HTTP-like enhancements  

## 🧠 Project Structure

Web_Server/
├── client_1.py # Simulates client with standard request
├── client_2.py # Simulates client with another request
├── client_3_empty_request_error.py # Tests empty/malformed request handling
├── server.py # Main custom server logic
├── html_files/
│ └── Login.html # Example static HTML content
├── unknown/
│ ├── empty.py # Handles edge cases / experiments
│ └── handling_http.py # Custom HTTP logic components

bash
Copy
Edit

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/python-custom-webserver.git
cd python-custom-webserver
2. Run the Server
bash
Copy
Edit
cd Web_Server
python server.py
3. Run a Client
bash
Copy
Edit
python client_1.py
# or
python client_2.py
4. Access Served HTML
Once the server is running, it will serve HTML files like Login.html. You can simulate client requests to these files.

📊 Sample Use Case
A user runs client_1.py which sends a GET request for Login.html. The server processes the request, logs it, and sends back the content of the HTML file. If the request is empty or the file doesn’t exist, appropriate error messages are handled gracefully.

📌 Future Improvements
Add support for more HTTP methods (POST, PUT, DELETE)

Implement routing and query parameter parsing

Integrate file upload and download capabilities

Build a browser-based UI for testing

Logging and monitoring tools for server status

👨‍💻 Author
Sumit1103
📧 sumitchandra960@gmail.com
