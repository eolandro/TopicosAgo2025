from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/login', methods=['POST'])
def login():
    return jsonify({"R": 200,"D": 100})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
