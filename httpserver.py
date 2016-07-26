#!/usr/bin/python

"""
Run with -> python httpserver.py 0.0.0.0 8001
or -> python httpserver.py 8001
or -> python httpserver.py

it logs headers and form data
"""

import cgi
import http.server
import logging
import socketserver
import sys

if len(sys.argv) > 2:
    PORT = int(sys.argv[2])
    I = sys.argv[1]
elif len(sys.argv) > 1:
    PORT = int(sys.argv[1])
    I = ""
else:
    PORT = 8080
    I = ""


def log_values(form):
    logging.warning("--  BEGIN VALUES")
    for item in form.list:
        logging.warning(item)
        logging.warning(dir(item))

    logging.warning("END VALUES --")
    logging.warning("\n")


def log_headers(headers):
    logging.warning("-- BEGIN HEADERS")
    logging.warning(headers)
    logging.warning("END HEADERS --")


class ServerHandler(http.server.SimpleHTTPRequestHandler):

    def do_get(self):
        logging.warning("======= HTTP GET STARTED =======")
        log_headers(self.headers)
        http.server.SimpleHTTPRequestHandler.do_GET(self)

    def do_post(self):
        logging.warning("======= HTTP POST STARTED =======")
        
        log_headers(self.headers)

        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD': 'POST',
                     'CONTENT_TYPE': self.headers['Content-Type'],
                     })
        
        log_values(form)

        http.server.SimpleHTTPRequestHandler.do_GET(self)


Handler = ServerHandler

httpd = socketserver.TCPServer(("", PORT), Handler)

print("Serving at...", PORT)
httpd.serve_forever()
