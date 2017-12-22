#!/usr/bin/python3
""" http_handler.py:
"""

# Import Required Libraries (Standard, Third Party, Local) ********************
from http.server import BaseHTTPRequestHandler, HTTPServer
import logging


# Authorship Info *************************************************************
__author__ = "Christopher Maue"
__copyright__ = "Copyright 2017, The B.O.B. Project"
__credits__ = ["Christopher Maue"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Christopher Maue"
__email__ = "csmaue@gmail.com"
__status__ = "Development"


# Http **************************************************
class MyHttpRequestHandler(BaseHTTPRequestHandler):
    def __init__(self, logger, gw, *args):
        self.logger = logger or logging.getLogger()
        self.gateway = gw
        self.filtered_request = str()
        self.dict = {}
        self.message = str()
        self.status = str()
        self.last_seen = str()
        self.name = str()
        self.addr = str()
        self.cmd = str()
        BaseHTTPRequestHandler.__init__(self, *args)


    def do_GET(self):
        # Decode request string
        self.logger.info('Processing request: %s', self.requestline)
        try:
            self.filtered_request = (self.requestline.split("?"))[1]
            self.filtered_request = (self.filtered_request.split(" "))[0]
            self.filtered_request = self.filtered_request.split("&")

            # Iterate through
            for item in self.filtered_request:
                try:
                    key, value = item.split('=')
                    self.dict[key] = value
                except Exception:
                    pass
                finally:
                    pass
            try:
                self.name = self.dict['name']
            except Exception:
                self.name = 'not defined'
            finally:
                pass
            try:
                self.addr = self.dict['addr']
            except Exception:
                self.addr = 'not defined'
            finally:
                pass
            try:
                self.cmd = self.dict['cmd']
            except Exception:
                self.cmd = 'not defined'
            finally:
                pass
        except Exception:
            self.status = 'invalid request'

        # Do the work here using the input parameters
        if self.cmd.lower() == 'ask' or self.cmd == '99':
            self.status, self.last_seen = self.gateway.read_status(name=self.name, addr=self.addr)
            self.status = 'state=' + self.status

        if self.cmd.lower() == 'on' or self.cmd == '1':
            self.status, self.last_seen = self.gateway.turn_on(name=self.name, addr=self.addr)
            self.status = 'state=' + self.status

        if self.cmd.lower() == 'off' or self.cmd == '0':
            self.status, self.last_seen = self.gateway.turn_off(name=self.name, addr=self.addr)
            self.status = 'state=' + self.status

        # Create and send response back to requester
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.message = "<html><body><h1>" + self.status + "</h1></body></html>"
        self.wfile.write(bytes(self.message, "utf8"))
        return
