#!/usr/bin/env python
# ~*~ coding: utf-8 ~*~
#
#   An async pixel-server implementation -- zoom!
#

import os
import time
import struct
import asyncio
import logging
from logging.handlers import RotatingFileHandler
from multiprocessing import Process

import uvloop

LOG_PATH = os.getenv('LOGPATH', 'access.log')

# create the folder our log files will go in, if it doesn't exist
folder, _ = os.path.split(os.path.abspath(LOG_PATH))
if not os.path.exists(folder):
    os.makedirs(folder)

# create an access log handler for GoAccess
formatter = logging.Formatter('%(message)s')
handler = RotatingFileHandler(LOG_PATH, maxBytes=500000, backupCount=5)
handler.setFormatter(formatter)
log = logging.getLogger('pix')
log.addHandler(handler)
log.setLevel(logging.DEBUG)


PIXEL_GIF = struct.pack(
    '<43B',
    71, 73, 70, 56, 57, 97, 1, 0, 1, 0, 128, 0, 0, 255, 255, 255,
    0, 0, 0, 33, 249, 4, 1, 0, 0, 0, 0, 44, 0, 0, 0, 0, 1, 0, 1,
    0, 0, 2, 2, 68, 1, 0, 59)
PIXEL_RESPONSE = (b'HTTP/1.1 200 OK',
                  b'Content-Type: image/gif',
                  b'Content-Length: 43',
                  b'Connection: close',
                  b'Accept-ranges: bytes',
                  b'',
                  PIXEL_GIF)
PIXEL_RESPONSE = b'\r\n'.join(PIXEL_RESPONSE)
TLS_ACCESS_DENIED = struct.pack(
    '<7B',
    0x15, 0x03, 0, 0, 0x02, 0x02, 0x31)


def process_data(data):
    lines = data.decode('utf-8').split('\r\n')
    method, route, version = lines.pop(0).split()
    proto, version_num = version.split('/')
    ret_data = {
        'Method': method,
        'Route': route,
        'Version': version_num,
        'Protocol': proto
    }
    for o in filter(None, lines):
        k, v = o.split(': ', 1)
        ret_data[k.strip()] = v.strip()
    return ret_data


class BaseProtocol(asyncio.Protocol):
    __slots__ = ['LOG_TEMPLATE', 'peer', 'start_time', 'transport']

    def __init__(self):
        super().__init__()
        self.peer = None
        self.transport = None
        self.start_time = None

    def connection_made(self, transport):
        self.start_time = time.time()
        self.peer = transport.get_extra_info('peername')
        self.transport = transport


class HTTPPixelProtocol(BaseProtocol):
    LOG_TEMPLATE = '{peer} [{time}] {host} "{method} {route} {protocol}/{version}" 200 43 "{user_agent}" {process_name}'

    def data_received(self, data):
        http_data = process_data(data)
        self.transport.write(PIXEL_RESPONSE)
        self.transport.close()
        log.info(self.LOG_TEMPLATE.format(
            peer=self.peer[0],
            time=time.strftime("%d/%b/%Y:%H:%M:%S %z", time.localtime(time.time())),
            host=http_data['Host'],
            method=http_data['Method'],
            route=http_data['Route'],
            protocol=http_data['Protocol'],
            version=http_data['Version'],
            user_agent=http_data['User-Agent'],
            process_name="pixelsrv"
        ))


class TLSNullProtocol(BaseProtocol):
    LOG_TEMPLATE = '{peer} [{time}] Unknown "GET unknown HTTP/1.1" 200 7 "Unknown" {process_name}'

    def data_received(self, data):
        self.transport.write(TLS_ACCESS_DENIED)
        self.transport.close()
        log.info(self.LOG_TEMPLATE.format(
            peer=self.peer[0],
            time=time.strftime("%d/%b/%Y:%H:%M:%S %z",
                               time.localtime(time.time())),
            process_name="pixelsrv-tls"
        ))


def run_server(host, port, protocol):
    loop = uvloop.new_event_loop()
    loop.set_debug(False)
    asyncio.set_event_loop(loop)
    routine = loop.create_server(protocol, host=host, port=int(port))
    server = loop.run_until_complete(routine)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    except Exception as e:
        logging.error(e)

    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()


if __name__ == "__main__":
    HTTP_HOST = os.getenv('HTTP_HOST', '0.0.0.0')
    HTTPS_HOST = os.getenv('HTTPS_HOST', '0.0.0.0')
    HTTP_PORT = os.getenv('HTTP_PORT', '8000')
    HTTPS_PORT = os.getenv('HTTPS_PORT', '8443')

    print('log: ', LOG_PATH)
    print('%s:%s' % (HTTP_HOST, HTTP_PORT))
    print('%s:%s' % (HTTPS_HOST, HTTPS_PORT))

    http = Process(target=run_server,
                   name='PixelServer',
                   args=(HTTP_HOST, HTTP_PORT, HTTPPixelProtocol))
    http.daemon = True

    https = Process(target=run_server,
                    name='NullServer',
                    args=(HTTPS_HOST, HTTPS_PORT, TLSNullProtocol))
    https.daemon = True

    http.start()
    https.start()

    try:
        http.join()

    except KeyboardInterrupt:
        http.terminate()
        https.terminate()
