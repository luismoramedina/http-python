#!/usr/bin/python

import http.server
import socketserver
import urllib
import urllib.request

PORT = 8000


class ServerHandler(http.server.SimpleHTTPRequestHandler):

    def do_get(self):
        print(self.path)
        new_path = 'http://localhost:8686' + self.path
        print(new_path)
        self.copyfile(urllib.request.urlopen(new_path), self.wfile)

Handler = ServerHandler
httpd = socketserver.TCPServer(("", PORT), Handler)

print("Listening on", PORT)

httpd.serve_forever()
