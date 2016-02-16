from router import Router


router = Router()

@router.route('/hello/<name>')
def hello(name):
   return 'Hello %s' % name

@router.route('/hello/<x:int>')
def handle_int(x):
    return 'int is %s' % x

@router.route('/hello/<action>/<param>')
def handle_action(action, param):
    return 'action is %s, param is %s' % (action, param)

@router.route('/hello/<x:path>')
def handle_path(x):
    return 'path is %s' % x

@router.route('/re/<x:re:a*b?c*>')
def handle_re(x):
    return 're is %s' % x




from wsgiref.simple_server import make_server

def hello_world_app(environ, start_response):
    status = '200 OK' # HTTP Status
    headers = [('Content-type', 'text/plain')] # HTTP Headers
    start_response(status, headers)

    func, args = router.match(environ)
    ret = func(**args)

    # The returned object is going to be printed
    return [ret.encode('utf-8')]

httpd = make_server('', 8000, hello_world_app)
print("Serving on port 8000...")

# Serve until process is killed
httpd.serve_forever()
