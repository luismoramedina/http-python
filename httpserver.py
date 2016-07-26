#!/usr/bin/python

"""
Run with -> python httpserver.py 0.0.0.0 8001
or -> python httpserver.py 8001
or -> python httpserver.py

it logs headers and form data
"""

import http.server
import socketserver
import logging
import cgi

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


def logValues(form):
    logging.warning("--  BEGIN VALUES")
    for item in form.list:
        logging.warning(item)
        logging.warning(dir(item))

    logging.warning("END VALUES --")
    logging.warning("\n")


def logHeaders(headers):
    logging.warning("-- BEGIN HEADERS")
    logging.warning(headers)
    logging.warning("END HEADERS --")

class ServerHandler(http.server.SimpleHTTPRequestHandler):

    def do_GET(self):
        logging.warning("======= HTTP GET STARTED =======")
        logHeaders(self.headers)
        http.server.SimpleHTTPRequestHandler.do_GET(self)

    def do_POST(self):
        logging.warning("======= HTTP POST STARTED =======")
        
        logHeaders(self.headers)

        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD':'POST',
                     'CONTENT_TYPE':self.headers['Content-Type'],
                     })
        
        logValues(form)

        http.server.SimpleHTTPRequestHandler.do_GET(self)


Handler = ServerHandler

httpd = socketserver.TCPServer(("", PORT), Handler)

print("Serving at...", PORT)
httpd.serve_forever()