#!/usr/bin/env python3
"""Start a local server to test the Aleo monitoring dashboard."""

import http.server
<<<<<<< HEAD
import os
import socketserver
=======
import socketserver
import os
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
import webbrowser
from pathlib import Path

PORT = 8080

<<<<<<< HEAD

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Add CORS headers
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        super().end_headers()


=======
class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Add CORS headers
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
def main():
    # Change to monitoring directory
    monitoring_dir = Path(__file__).parent
    os.chdir(monitoring_dir)
<<<<<<< HEAD

=======
    
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
    print(f"Starting dashboard server on http://localhost:{PORT}")
    print("\nAvailable dashboards:")
    print(f"1. Live Dashboard: http://localhost:{PORT}/dashboard-live.html")
    print(f"2. Mock Dashboard: http://localhost:{PORT}/dist/index.html")
    print(f"3. Test Connection: http://localhost:{PORT}/test-live-connection.html")
    print("\nPress Ctrl+C to stop the server")
<<<<<<< HEAD

    with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
        # Try to open browser
        try:
            webbrowser.open(f"http://localhost:{PORT}/dashboard-live.html")
        except:
            pass

        httpd.serve_forever()


=======
    
    with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
        # Try to open browser
        try:
            webbrowser.open(f'http://localhost:{PORT}/dashboard-live.html')
        except:
            pass
        
        httpd.serve_forever()

>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nServer stopped.")
    except Exception as e:
<<<<<<< HEAD
        print(f"Error: {e}")
=======
        print(f"Error: {e}")
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
