#!/usr/bin/env python

# A Pixel Server

import logging
import os
import socketserver
import struct, sys, signal, time
import threading
import time

from datetime import datetime

logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%Y-%m-%d %I:%M:%S',
                    filename=os.environ['PIXELSERV_LOGFILE'], level=logging.INFO)
HOST, PORT = "0.0.0.0", 80
HOST_TLS, PORT_TLS = "0.0.0.0", 443


def parse_request(self):
    fields = ['verb', 'path', 'version']
    self.request_data = {f:'' for f in fields}

    line = self.rfile.readline(65536)
    host = line.rstrip(bytes('\r\n', "utf-8")).split()
    req = self.data.rstrip(bytes('\r\n', 'utf-8')).split()

    try:
        if host[1]:
            self.request_data['host'] = host[1]
    except Exception:
        pass

    for idx,field in enumerate(req):
        self.request_data[fields[idx]] = field

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

class PixelRequestHandler(socketserver.StreamRequestHandler):

    pixel = struct.pack('<43B',
            71, 73, 70, 56, 57, 97, 1, 0, 1, 0, 128, 0, 0, 255, 255, 255,
            0, 0, 0, 33, 249, 4, 1, 0, 0, 0, 0, 44, 0, 0, 0, 0, 1, 0, 1,
            0, 0, 2, 2, 68, 1, 0, 59)

    def handle(self):
        S = ("HTTP/1.1 200 OK\r\n"
             "Content-type: image/gif\r\n"
             "Accept-ranges: bytes\r\n"
             "Content-length: 43\r\n\r\n")

        self.wfile.write(bytes(S, "utf-8"))
        self.wfile.write(self.pixel)
        self.data = self.rfile.readline(65536)
        parse_request(self)
        client_ip   = self.client_address[0]
        decoded_req_data = {k:v.decode("utf-8") for k,v in self.request_data.items()}
        logging.info('{client_ip} {verb} {host}{path}'.format(client_ip=client_ip,**decoded_req_data))
        sys.stdout.flush()


class TLSRequestHandler(socketserver.StreamRequestHandler):

    def handle(self):
        S= ('\x15',         # Alert 21
            '\x03', '\x00', # Version 3.0
            '\x00', '\x02', # Length == 2
            '\x02', # Fatal event
            '\x31') # 0x31 == TLS access denied (49)

        self.wfile.write(bytes(''.join(S), "utf-8"))
        self.data = self.rfile.readline(65536)
        parse_request(self)
        client_ip   = self.client_address[0]
        logging.info('{client_ip} - - (TLS)'.format(client_ip=client_ip))
        sys.stdout.flush()

def sighandler(signal, frame):
    raise Exception('Recieved %s signal' % signal)

if __name__ == "__main__":
    server = ThreadedTCPServer((HOST, PORT), PixelRequestHandler)
    tls_server = ThreadedTCPServer((HOST_TLS, PORT_TLS), TLSRequestHandler)
    try:
        signal.signal(signal.SIGINT, sighandler)

        pixel_server = threading.Thread(target=server.serve_forever)
        tls_server = threading.Thread(target=tls_server.serve_forever)

        pixel_server.setDaemon(True)
        tls_server.setDaemon(True)

        pixel_server.start()
        tls_server.start()
        while True:
            time.sleep(1)
    except:
        sys.exit(0)
