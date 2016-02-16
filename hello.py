#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from router import Router
import re
import urllib


router = Router()


# test URL: localhost:8000/int/10
# expected: 10 is of <class 'int'>
@router.route('/int/<x:int>')
def handle_int(x):
    return '%d is of %s' % (x, type(x))

# test URL: localhost:8000/float/20.32
# expected: 20.320000 is of <class 'float'>
@router.route('/float/<x:float>')
def handle_float(x):
    return '%f is of %s' % (x, type(x))

# test URL: localhost:8000/hello/world
# expected: Hello world
# test URL: localhost:8000/hello/中国
# expected: Hello 中国
@router.route('/hello/<name>')
def hello(name):
    return 'Hello %s' % name

# test URL: localhost:8000/hello/minus/10
# expected: action is minus, param is 10
@router.route('/hello/<action>/<param>')
def handle_action(action, param):
    return 'action is %s, param is %s' % (action, param)

# test URL: localhost:8000/hello/world/I/love/you
# expected: path is world/I/love/you
@router.route('/hello/<x:path>')
def handle_path(x):
    return 'path is %s' % x

# test URL: localhost:8000/re/aaabccc
# expected: re is aaabccc
@router.route('/re/<x:re:a*b?c*>')
def handle_re(x):
    return 're is %s' % x


# test URL: localhost:8000/another/test:router
# expected: another handler: action is test, param is router
def another_handler(action, param):
    return 'another handler: action is %s, param is %s' % (action, param)
router.route('/another/<action>:<param>', callback=another_handler)



# Add custom filter / taken and modified from bottle.py
def list_filter(config):
    ''' Matches a comma separated list of numbers. '''
    delimiter = config or ','
    regexp = r'\d+(%s\d)*' % re.escape(delimiter)

    def to_python(match):
        return map(int, match.split(delimiter))
    return regexp, to_python

router.add_filter('list', list_filter)


# test URL: localhost:8000/list/1,2,3,4,5
# expected: lst is [1, 2, 3, 4, 5]
@router.route('/list/<lst:list>')
def list_handler(lst):
    return 'lst is %s' % str([x for x in lst])



from wsgiref.simple_server import make_server

def hello_world_app(environ, start_response):
    status = '200 OK' # HTTP Status
    headers = [('Content-type', 'text/plain; charset=utf-8')] # HTTP Headers
    start_response(status, headers)

    # decode url
    path = environ['bottle.raw_path'] = environ['PATH_INFO']
    environ['PATH_INFO'] = path.encode('latin1').decode('utf8', 'ignore')

    try:
        func, args = router.match(environ)
        ret = func(**args)
    except:
        ret = '404'

    # The returned object is going to be printed
    return [ret.encode('utf-8')]

httpd = make_server('', 8000, hello_world_app)
print("Serving on port 8000...")

# Serve until process is killed
httpd.serve_forever()
