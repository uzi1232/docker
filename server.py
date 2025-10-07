import argparse
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from env_var import get_config_file_value, get_env_var

config_path_env = ""

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
        elif self.path == "/configValue":
            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(get_config_file_value("configValue", config_path_env).encode("utf-8"))
        elif self.path == "/envValue":
            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(get_env_var("envValue", "").encode("utf-8"))
        elif self.path == "/secretValue":
            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(get_config_file_value(".secretValue", config_path_env).encode("utf-8"))            
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
    parser = argparse.ArgumentParser(
                    prog='HTTP server',
                    description='Serves different endpoints for COMP 4016 assignments')
    parser.add_argument('-H', '--host', required=True, type=str)
    parser.add_argument('-p', '--port', required=True, type=int)
    parser.add_argument('-c', '--config_env', type=str, default="CONFIG_PATH")
    args = parser.parse_args()
    config_path_env = args.config_env
    server = HTTPServer((args.host, args.port), HttpHandler)
    server.serve_forever()
