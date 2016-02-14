#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from wsgiref.simple_server import make_server

class Router():
    """route->targe collection"""
    def __init__(self, arg):
        super(Router, self).__init__()
        self.arg = arg


class Simple():
    """Simple Web Application"""
    def __init__(self):
        self.routes = []
        self.router = Router()
        pass

    def route(self, path=None, method='GET'):
        """Add a route for current application"""
        pass

    def _handle(self, environ):
        """Actual handler for wsgi request, get the route and pass"""
        route, args = self.router.match(environ)
        return route.call(**args)

    def wsgi_handler(self, environ, start_response):
        """Handler for wsgi application, mainly handle the response header"""
        output = self._handle(environ)
        start_response('200 OK', [('content-type', 'text/plain')])
        return output

    def __call__(self, environ, start_response):
        """An application itself can be called as a normal application"""
        return self.wsgi_handler(environ, start_response)

def route(arg0):
    """Decorator for route"""
    def decorator(arg1):
        """TODO: Docstring for decorator."""
        pass
    return decorator

def run(app = None,
        host = '127.0.0.1',
        port = 8080):
    """Start a server instance"""
    server = make_server(host, port, app)
    server.serve_forever()
