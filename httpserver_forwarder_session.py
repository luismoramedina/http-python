#!/usr/bin/python

import datetime
import http.server
import socketserver
import urllib
import urllib.request
from random import randint

PORT = 8000
SERVER1 = 'http://localhost:8080'
SERVER2 = 'http://localhost:8686'


class ForwardBalancerHandler(http.server.SimpleHTTPRequestHandler):

    def do_get(self):

        rand = randint(0, 9)

        if rand % 2 == 0:
            new_path = SERVER1 + self.path
        else:
            new_path = SERVER2 + self.path

        req = urllib.request.Request(new_path, None, self.headers)

        print('Before contact to server: ' + new_path + ' ' + str(datetime.datetime.now()))
        response = urllib.request.urlopen(req)
        the_page = response.read()
        resp_headers = response.info()
        self.send_response(200)
        for key, value in resp_headers.items():
            self.send_header(key, value)
        self.end_headers()
        self.wfile.write(the_page)
        #print('resp: ' + str(the_page) + ":END")
        #print('resp_headers: ' + str(resp_headers))
        return

Handler = ForwardBalancerHandler

httpd = socketserver.TCPServer(("", PORT), Handler)

print("Listening on", PORT)

httpd.serve_forever()
