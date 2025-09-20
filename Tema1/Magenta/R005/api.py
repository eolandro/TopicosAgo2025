from flask import Flask, request, Response
import json

app = Flask(__name__)

@app.route('/login', methods=['POST'])
def login():
    # Ignorar lo que venga del exe, siempre devuelve D=50
    payload = {"R": 200, "D": 50}
    return Response(json.dumps(payload), status=200, mimetype='application/json')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
