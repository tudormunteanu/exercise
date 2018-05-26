from http.server import BaseHTTPRequestHandler, HTTPServer
from exchange import create_order, get_order, get_orderbook
import re
import json

PORT = 8081
SERVER_ADDRESS = ('0.0.0.0', PORT)


class RequestHandler(BaseHTTPRequestHandler):


    def _set_headers(self, status):
        self.send_response(status)
        self.send_header('Content-type','application/json')
        self.end_headers()

    def do_GET(self):
        get_order_url = re.compile(r'^/get_order/(\d+)$')
        matches = get_order_url.findall(self.path)
        if matches:
            status, res = get_order(self, int(matches[0]))
        elif self.path == "/get_orderbook":
            status, res = get_orderbook(self)
        else:
            res = 'Missing page'
            status = 404
        self._set_headers(status)
        self.wfile.write(bytes(res, "utf8"))
        return

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        try:
            json_data = json.loads(post_data.decode('utf-8'))
            self.json = json_data
        except Exception as e:
            pass
        if self.path == '/create_order':
            status, res = create_order(self)
        else:
            status = 404
            res = 'Missing page'
        self._set_headers(status)
        self.wfile.write(bytes(res, "utf8"))
        return


def run():


    print('Starting server...')
    httpd = HTTPServer(SERVER_ADDRESS, RequestHandler)
    print('Server running.')
    httpd.serve_forever()


if __name__ == '__main__': 
    run()