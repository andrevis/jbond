from http.server import HTTPServer, BaseHTTPRequestHandler
from logger import *
from threading import Thread
import ssl
import mimetypes

logger = logging.getLogger("Http")

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        logger.info(f'Incoming POST request: {self.path}:\n{self.request}')

        self.send_response(200)
        self.send_header('Content-Length', 0)
        self.end_headers()

    def do_GET(self):
        logger.info(f'Incoming GET request: {self.path}')

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
                self.end_headers()
                self.wfile.write(content)

        except:
            self.send_response(404)
            self.send_header('Content-Length', 0)
            self.end_headers()

class HttpServer(Thread):
    __httpd__ = None

    def __init__(self, port):
        super().__init__(name = 'HttpServer')
        self.__httpd__ = HTTPServer(('0.0.0.0', port), SimpleHTTPRequestHandler)
        self.__httpd__.socket = ssl.wrap_socket(self.__httpd__.socket,
            keyfile = '/etc/letsencrypt/live/jbond-app.ru/privkey.pem',
            certfile = '/etc/letsencrypt/live/jbond-app.ru/cert.pem', server_side = True)

        logger.info(f'Starting httpd server on port {port}...')

    def run(self):
        self.__httpd__.serve_forever()