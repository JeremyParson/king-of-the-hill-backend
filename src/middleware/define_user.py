from werkzeug.wrappers import Request, Response, ResponseStream
import jwt
from jwt import InvalidTokenError 
# Define the user from request


class middleware():
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        request = Request(environ)
        try:
            if request.headers.get("Authorization"):
                token = request.headers.get("Authorization").split(" ")
                if token[0] == 'Bearer':
                    content = jwt.decode(token[1], "secret", algorithms=["HS256"])
                    environ['user'] = {'id': content['id']}
                    return self.app(environ, start_response)
        except InvalidTokenError:
            pass

        environ['user'] = None
        return self.app(environ, start_response)
