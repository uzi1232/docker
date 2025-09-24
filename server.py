import json
from http.server import BaseHTTPRequestHandler, HTTPServer

def get_json(message):
    try:
        return json.loads(message)
    except Exception as exp:
        return None

class HttpHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/foo":
            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(b"bar")
        elif self.path == "/kill":
            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(b"Stopping the server.")
            exit(0)
        else:
            response = f"{self.path} not found."
            self.send_response(404)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(response.encode("utf-8"))

    def do_POST(self):
        if self.path == "/hello":
            content_length = int(self.headers['Content-Length'])
            request_body = self.rfile.read(content_length)
            print("Received POST data:", request_body.decode())
            request = get_json(request_body.decode())
            if request is not None:
                if ("name" in request):
                    response = f"Hello {request['name']}"
                    self.send_response(200)
                else:
                    response = f"Key 'name' not found"
                    self.send_response(404)
            else:
                response = f"Request JSON could not be parsed."
                self.send_response(400)

            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(response.encode("utf-8"))

if __name__ == "__main__":
    SERVER_PORT = 8080
    server = HTTPServer(("0.0.0.0", 8080), HttpHandler)
    server.serve_forever()
