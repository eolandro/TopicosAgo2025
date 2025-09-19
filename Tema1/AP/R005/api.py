from bottle import post, run

@post("/login")
def login():
    print("Acceso concedido automáticamente")
    return {"R":200,"D":50}

run(host='0.0.0.0', port=8080)