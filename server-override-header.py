import http.server
import socketserver
import urllib
import urllib.request

class ContentTypeOverwriteHeaderHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        print(self.path)
        self.send_response(200)
        self.send_header("Content-Type", "application/json;charset=utf-8")
        self.end_headers()
        self.copyfile(open('.' + self.path, 'rb'), self.wfile)

server = socketserver.TCPServer(("", 8000), ContentTypeOverwriteHeaderHandler)
server.serve_forever()
