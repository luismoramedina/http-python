#!/usr/bin/python

"""
Run with -> python httpserver_forwarder.py 0.0.0.0 8001
or -> python httpserver.py 8001
or -> python httpserver.py

it forwards request to another server
"""

import datetime
import urllib
import urllib.request
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
    PORT = 8000
    I = ""


class ServerHandler(http.server.SimpleHTTPRequestHandler):

    def do_GET(self):
        print ("======= GET STARTED =======")
        print (self.headers)
        http.server.SimpleHTTPRequestHandler.do_GET(self)

    def do_POST(self):
        print ("======= POST STARTED =======")
        print ("path: ", self.path)
        
        if self.path.startswith('/Globales/XML'):
            replaced_path = self.path.replace('/Globales', '')
            new_path = 'http://localhost:9080/TESTWS_ENS' + replaced_path
            print ("REDIRECTING!!! to ", new_path)
            print (self.wfile)
            print (self)

            form = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={'REQUEST_METHOD':'POST',
                         'CONTENT_TYPE':self.headers['Content-Type'],
                         })

            values = {}

            for key in form.keys():
                variable = str(key)
                value = str(form.getvalue(variable))
                values[variable] = value

            data =  urllib.parse.urlencode(values)
            data = data.encode('utf-8') # data should be bytes
            #req = urllib.request.Request(new_path, data, self.headers)
            req = urllib.request.Request(new_path, data)
            print (self.headers)

            print ('Before contact to server: ' + str(datetime.datetime.now()))
            response = urllib.request.urlopen(req)
            print ('After contact to server: ' + str(datetime.datetime.now()))
            the_page = response.read()
            print('resp: ' + str(the_page))
            resp_headers = response.info()
            print('resp_headers: ' + str(resp_headers))
            for key, value in resp_headers.items():
                self.send_header(key, value)
            self.end_headers()

            self.wfile.write(the_page)
            self.send_response(200)

            #self.copyfile(urllib.request.urlopen(new_path), self.wfile)

        #http.server.SimpleHTTPRequestHandler.do_POST(self)

Handler = ServerHandler

httpd = socketserver.TCPServer(("", PORT), Handler)

print ("Listening on %s", PORT)

httpd.serve_forever()