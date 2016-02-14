from simple import Simple

app = Simple()

@app.route('/hello')
def hello():
    return "Hello World!"

app.run(host='localhost', port=8080)
