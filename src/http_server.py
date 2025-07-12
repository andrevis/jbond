from http.server import HTTPServer, SimpleHTTPRequestHandler
from threading import Thread
import ssl
import mimetypes
import asyncio
import json

from filters import parse_filters
from bonds.getter import BondsGetter
from logger import *
from bot import *
from messages import *

logger = logging.getLogger("Http")


class HTTPRequestHandler(SimpleHTTPRequestHandler):
    __bonds_getter__ = BondsGetter()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # self.send_header('Transfer-Encoding', 'chunked')
        # for chunk in response.iter_content(chunk_size=1024):
        #     chunk_header = f'{len(chunk):x}\r\n'.encode('utf-8')
        #     self.wfile.write(chunk_header)
        #     self.wfile.write(chunk)
        #     self.wfile.write(b'\r\n')
        # self.wfile.write(b'0\r\n\r\n')

    def __send_response__(self, code, content_type=None, data=None):
        self.send_response(code)
        self.send_header('Content-Length', int(len(data) if data else 0))
        self.send_header('Connection', 'close')
        if content_type:
            self.send_header('Content-Type', content_type)
        self.end_headers()
        if data:
            self.wfile.write(data)

    def do_POST(self):
        try:
            logger.info(f'Incoming POST {self.path} from {self.client_address}')

            content_length = int(self.headers['Content-Length'])

            if self.path == '/filters' and content_length > 0:
                filters = parse_filters(self.rfile.read(content_length))

                json_bonds = self.__bonds_getter__.get(filters)
                if not json_bonds:
                    self.__send_response__(500)
                    return

                self.__send_response__(200, 'application/json', bytes(json.dumps(json_bonds, indent=0), 'utf-8'))

                message_pack = MessagePack(filters)
                for paper in json_bonds:
                    message_pack.append(SendMessageTask(filters.chat_id, paper))

                if len(message_pack) > 0:
                    messages_queue.put(message_pack)

            else:
                self.__send_response__(400)
                return
        except Exception as e:
            logger.error(f'POST {self.path} exception: {e}')
            self.__send_response__(500)


    def do_GET(self):
        logger.info(f'Incoming GET {self.path} from {self.client_address}')

        if self.path == '/' or len(self.path) == 0:
            self.path = '/index.html'

        try:
            path = '/opt/jbond/html/' + self.path
            mime_type, _ = mimetypes.guess_type(path)

            with open(path, 'rb') as file:
                content = file.read()
                self.send_response(200)
                self.send_header('Content-Type', f'{mime_type}')
                self.send_header('Content-Length', len(content))
                self.send_header('Connection', 'close')
                self.end_headers()
                self.wfile.write(content)

        except:
            self.send_response(404)
            self.send_header('Content-Length', 0)
            self.send_header('Connection', 'close')
            self.end_headers()

class HttpServer(Thread):
    __port__ = None
    __httpd__ = None

    def __init__(self, port):
        super().__init__(name = 'HttpServer')
        self.__port__ = port

        HTTPServer.allow_reuse_address = True
        self.__httpd__ = HTTPServer(('0.0.0.0', self.__port__), HTTPRequestHandler)

        self.__httpd__.timeout = 1
        self.__httpd__.socket = ssl.wrap_socket(self.__httpd__.socket,
            keyfile = '/etc/letsencrypt/live/jbond-app.ru/privkey.pem',
            certfile = '/etc/letsencrypt/live/jbond-app.ru/cert.pem', server_side = True)

        logger.info(f'Starting httpd server on port {self.__port__}...')
        self.start()

    def run(self):
        try:
            self.__httpd__.serve_forever()
        except Exception as e:
            logger.info(f'HttpServer error: {e}')
        finally:
            logger.info(f'Stopping httpd server on port {self.__port__}...')
            self.__httpd__.server_close()