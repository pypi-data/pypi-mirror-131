import base64
import http
import json
import os
from http.server import HTTPServer, CGIHTTPRequestHandler
import httpretty
from httpretty.core import HTTPrettyRequest

PORT = '8756'
PATH = '/tests/resources/'


class SimpleHandler(CGIHTTPRequestHandler):
    def do_HEAD(self) -> None:
        if 'key' in self.requestline or 'value' in self.requestline:
            self.send_response(http.HTTPStatus.OK)
            self.send_header("params", 'key:value')
            self.end_headers()
            return
        f = self.send_head()
        if f:
            f.close()


def start_serve():
    """This method allow us to launch a small http server for our tests."""
    server_address = ("", int(PORT))
    server = http.server.HTTPServer
    handler = SimpleHandler
    handler.cgi_directories = [""]

    httpd = server(server_address, handler)
    httpd.serve_forever()


class CustomServerHandler(http.server.BaseHTTPRequestHandler):

    def do_HEAD(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_AUTHHEAD(self):
        self.send_response(401)
        self.send_header(
            'WWW-Authenticate', 'Basic realm="Demo Realm"')
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_GET(self):
        key = self.server.get_auth_key()

        ''' Present frontpage with user authentication. '''
        if self.headers.get('Authorization') is None:
            self.do_AUTHHEAD()

            response = {
                'success': False,
                'error': 'No auth header'
            }

            self.wfile.write(bytes(json.dumps(response), 'utf-8'))

        elif self.headers.get('Authorization') == 'Basic ' + str(key):
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()

            response = {
                'path': self.path,
            }

            self.wfile.write(bytes(json.dumps(response), 'utf-8'))
        else:
            self.do_AUTHHEAD()

            response = {
                'success': False,
                'error': 'Invalid credentials'
            }

            self.wfile.write(bytes(json.dumps(response), 'utf-8'))


class CustomHTTPServer(http.server.HTTPServer):
    key = ''

    def __init__(self, address, handlerClass=CustomServerHandler):
        super().__init__(address, handlerClass)

    def set_auth(self, username, password):
        self.key = base64.b64encode(
            bytes('%s:%s' % (username, password), 'utf-8')).decode('ascii')

    def get_auth_key(self):
        return self.key


def start_auth_serve():
    server = CustomHTTPServer(('', int(PORT)))
    server.set_auth('user', 'pwd123456')
    server.serve_forever()


def start_mock_oauth2_serve(service: str):
    resource_dir = os.path.join(os.path.dirname(__file__), 'resources')
    service_uri = f'{service}'
    resource = "https://something.com/resources/test.txt"
    not_resource = "https://something.com/resources/not_here.txt"
    token_url = "https://something.com/resources/token"
    bad_token_url = "https://something.com/resources/bad_token"

    def download(request: HTTPrettyRequest, uri, headers):
        body = request.headers
        print()
        if 'new_token' in body.get('Authorization'):
            return 200, headers, b'This is my awesome test.'

        with open(os.path.join(resource_dir, 'wrong_user.json')) as f:
            data = f.read()
        return 401, headers, data

    def token_request(request: HTTPrettyRequest, uri, headers):
        if 'password' in request.parsed_body.get('grant_type'):
            response = '{"access_token": "new_token", ' \
                       ' "expires_in":300,'\
                       ' "refresh_expires_in":1800, ' \
                       ' "refresh_token": "XXXXXX", '\
                       ' "token_type":"bearer",'\
                       ' "not-before-policy":1620204142,' \
                       ' "session_state":"a371d927-44dd-42b6-ba7d-",' \
                       ' "scope":"email profile"}'

        elif 'refresh_token' in request.parsed_body.get('grant_type'):
            response = '{"access_token": "refresh_token",'\
                       ' "expires_in":300,'\
                       ' "refresh_expires_in":1800,' \
                       ' "refresh_token": "XXXXXX", '\
                       ' "token_type":"bearer",'\
                       ' "not-before-policy":1620204142,' \
                       ' "session_state":"a371d927-44dd-42b6-ba7d-",' \
                       ' "scope":"email profile"}'
        else:
            raise ValueError(
                f"Wrong grant_type {request.parsed_body.get('grant_type')}")
        return 200, headers, response

    def bad_token_request(request: HTTPrettyRequest, uri, headers):
        return 401, headers, "Bad token!"

    def not_found(request: HTTPrettyRequest, uri, headers):
        return 404, headers, 'File not found'

    httpretty.enable()
    httpretty.register_uri(httpretty.GET, resource, download)
    httpretty.register_uri(httpretty.GET, not_resource, not_found)
    httpretty.register_uri(httpretty.POST, token_url, token_request)
    httpretty.register_uri(httpretty.POST, bad_token_url, bad_token_request)


def stop_mock_oauth2_serve():
    httpretty.disable()
    httpretty.reset()
