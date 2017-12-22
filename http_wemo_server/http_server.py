#!/usr/bin/python3
""" http_handler.py:
"""

# Import Required Libraries (Standard, Third Party, Local) ********************
from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
import os
import sys
if __name__ == "__main__":
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from http_wemo_server.configure import ConfigureService
from http_wemo_server.wemo import WemoAPI
from http_wemo_server.request_handler import MyHttpRequestHandler


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
class HttpServer(object):
    def __init__(self, logger, gw):
        # Configure loggers
        self.logger = logger or logging.getLogger(__name__)
        # Define instance variables
        self.gateway = gw

        def handler(*args):
            MyHttpRequestHandler(self.logger, self.gateway, *args)

        self.logger.info('Starting server')
        self.server = HTTPServer(('', 8000), handler)
        self.logger.info('Server is running')
        self.server.serve_forever()


if __name__ == '__main__':
    PARENT_PATH = os.path.dirname(os.path.abspath(__file__))
    CONFIG_FILE = os.path.join(PARENT_PATH, 'config.ini')
    print("\n\nUsing Config file:\n" + CONFIG_FILE + "\n\n")
    SERVICE_CONFIG = ConfigureService(CONFIG_FILE)
    LOGGER = SERVICE_CONFIG.get_logger()
    LOGGER.info('Creating WEMO gateway object')
    WEMO_GW = WemoAPI(LOGGER)
    LOGGER.info('Creating HTTP server object')
    HTTP_SERVER = HttpServer(LOGGER, gw=WEMO_GW)
