from bottle import route, run, template, post,request

@route('/hello/<name>')
def index(name):
    return template('<b>Hello {{name}}</b>!', name=name)

@post('/loginnnnn')
def login():
    
    if not "USR" in request.json:
        return {"R":400,"D":"No ta el USR pa"}
    if not "PASS" in request.json:
        return {"R":400,"D":"No ta el pass pa"}
    return {"R":200,"D":50}

run(host='localhost', port=8080)
