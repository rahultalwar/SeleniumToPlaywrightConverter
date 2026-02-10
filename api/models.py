import json
from http.server import BaseHTTPRequestHandler

AVAILABLE_MODELS = ["moonshot-v1-8k", "moonshot-v1-32k", "moonshot-v1-128k"]
DEFAULT_MODEL = "moonshot-v1-8k"

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        response = {
            'models': AVAILABLE_MODELS,
            'default': DEFAULT_MODEL
        }
        self.wfile.write(json.dumps(response).encode())
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
