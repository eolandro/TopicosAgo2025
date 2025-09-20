from bottle import post, run, request

intentos = 50

@post("/login")
def login():
    return {"R":200,"D":intentos}

run(host='0.0.0.0', port=8000)
