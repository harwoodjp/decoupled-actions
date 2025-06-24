#!/usr/bin/env python3
import os
import sys
import json
import importlib.util
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

def load_action(action_name):
    """Load an action module from the actions directory."""
    action_path = os.path.join("actions", f"{action_name}.py")
    
    if not os.path.exists(action_path):
        return None
    
    spec = importlib.util.spec_from_file_location(action_name, action_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    
    return module

class ActionHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        """Handle POST requests to execute actions."""
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            request_data = json.loads(post_data.decode('utf-8'))
            
            action_name = request_data.get('action')
            args = request_data.get('args', [])
            
            if not action_name:
                self.send_error_response(400, "Missing 'action' field")
                return
            
            # Load and execute the action
            action_module = load_action(action_name)
            if not action_module:
                self.send_error_response(404, f"Action '{action_name}' not found")
                return
            
            if not hasattr(action_module, 'run'):
                self.send_error_response(500, f"Action '{action_name}' missing run function")
                return
            
            result = action_module.run(args)
            
            self.send_json_response(200, {
                "success": True,
                "action": action_name,
                "args": args,
                "result": result
            })
            
        except json.JSONDecodeError:
            self.send_error_response(400, "Invalid JSON in request body")
        except Exception as e:
            self.send_error_response(500, f"Error executing action: {str(e)}")
    
    def do_GET(self):
        """Handle GET requests to execute actions with query parameters."""
        try:
            parsed_url = urlparse(self.path)
            query_params = parse_qs(parsed_url.query)
            
            action_name = query_params.get('action', [None])[0]
            args = query_params.get('args', [])
            
            if not action_name:
                self.send_error_response(400, "Missing 'action' parameter")
                return
            
            # Load and execute the action
            action_module = load_action(action_name)
            if not action_module:
                self.send_error_response(404, f"Action '{action_name}' not found")
                return
            
            if not hasattr(action_module, 'run'):
                self.send_error_response(500, f"Action '{action_name}' missing run function")
                return
            
            result = action_module.run(args)
            
            self.send_json_response(200, {
                "success": True,
                "action": action_name,
                "args": args,
                "result": result
            })
            
        except Exception as e:
            self.send_error_response(500, f"Error executing action: {str(e)}")
    
    def send_json_response(self, status_code, data):
        """Send a JSON response."""
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))
    
    def send_error_response(self, status_code, message):
        """Send an error response."""
        self.send_json_response(status_code, {
            "success": False,
            "error": message
        })
    
    def log_message(self, format, *args):
        """Override to customize log format."""
        print(f"{self.address_string()} - {format % args}")

def main():
    """Start the HTTP server."""
    port = 8000
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            print("Invalid port number")
            return 1
    
    server_address = ('', port)
    httpd = HTTPServer(server_address, ActionHandler)
        
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped")
        httpd.server_close()
        return 0

if __name__ == "__main__":
    sys.exit(main())