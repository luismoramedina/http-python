#!/usr/bin/python

"""
Run with -> python httpserver.py 0.0.0.0 8001
or -> python httpserver.py 8001
or -> python httpserver.py

it emulates an authenticated
"""

import http.server
import logging
import socketserver


class ServerHandler(http.server.SimpleHTTPRequestHandler):

    def do_GET(self):
        logging.warning("======= GET STARTED =======")
        logging.warning(self.headers)

        self.send_response(401)
        self.send_header("Content-Type", "text/html;charset=utf-8")
        self.send_header("WWW-Authenticate", 'Digest realm="My Digest Secure REST-WS", qop="auth", nonce="MTMxNzA1MDEwOTk0MTo0MmZhNWIyMjkzYWQwN2U3MGM2YjY1N2UzYTZhMWM3NA=="')
        self.end_headers()
#        self.wfile.write("")

Handler = ServerHandler

httpd = socketserver.TCPServer(("", 8000), Handler)

httpd.serve_forever()