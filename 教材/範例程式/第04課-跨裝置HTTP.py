import socket
from http.server import BaseHTTPRequestHandler, HTTPServer

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        body = b'Hello, AIoT!'
        self.send_response(200)
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)
        print('Request handled: 200')
    def log_message(self, format, *args):
        pass

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as probe:
    probe.connect(('1.1.1.1', 53))
    address = probe.getsockname()[0]
with HTTPServer((address, 0), Handler) as server:
    server.timeout = 120
    print('Ready port:', server.server_port, flush=True)
    server.handle_request()
print('Server closed')
