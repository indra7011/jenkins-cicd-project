from http.server import HTTPServer, BaseHTTPRequestHandler

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b"Hello, this is my Jenkins CI/CD Pipeline project running successfullyfdsgsssssssssfffffafsaddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd!")

httpd = HTTPServer(('0.0.0.0', 80), SimpleHTTPRequestHandler)
print("Server running on port 80...")
httpd.serve_forever()
