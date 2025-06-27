from http.server import HTTPServer, BaseHTTPRequestHandler, SimpleHTTPRequestHandler
from logger import *
from threading import Thread
import ssl
import mimetypes

logger = logging.getLogger("Http")

class HTTPRequestHandler(SimpleHTTPRequestHandler):
    def do_POST(self):
        logger.info(f'Incoming POST {self.path} from {self.client_address}')

        if self.path == '/filters':
            file_length = int(self.headers['Content-Length'])
            filters = self.rfile.read(file_length)
            logger.info(f'Received filters: {filters}')

            self.send_response(200)
        else:
            self.send_response(400)

        self.send_header('Content-Length', 0)
        self.send_header('Connection', 'close')
        self.end_headers()

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

    def run(self):
        try:
            self.__httpd__.serve_forever()
        except Exception as e:
            logger.info(f'HttpServer error: {e}')
        finally:
            logger.info(f'Stopping httpd server on port {self.__port__}...')
            self.__httpd__.server_close()
