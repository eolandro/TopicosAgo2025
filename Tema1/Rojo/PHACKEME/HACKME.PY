import threading
import socket
from bottle import Bottle, run, post, request


app = Bottle()

@app.route('/')
def index():
    return "<h2>Servidor Bottle funcionando</h2>"

@app.post('/login')
def login():
    
    return {"R": 200, "D": 199}

def run_bottle():
    
    run(app, host='127.0.0.1', port=8080, debug=True)


PROXY_HOST = '45.76.183.114'  
PROXY_PORT = 8080
LOCAL_HOST = '127.0.0.1'
LOCAL_PORT = 8080

def handle_client(client_socket):
    remote = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    remote.connect((LOCAL_HOST, LOCAL_PORT))

    def forward(source, destination):
        try:
            while True:
                data = source.recv(4096)
                if not data:
                    break
                destination.sendall(data)
        except:
            pass
        finally:
            source.close()
            destination.close()

    t1 = threading.Thread(target=forward, args=(client_socket, remote))
    t2 = threading.Thread(target=forward, args=(remote, client_socket))
    t1.start()
    t2.start()

def run_proxy():
    proxy = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    proxy.bind((PROXY_HOST, PROXY_PORT))
    proxy.listen(5)
    print(f"[+] Proxy escuchando en {PROXY_HOST}:{PROXY_PORT}")

    while True:
        client, addr = proxy.accept()
        print(f"[+] Conexión entrante de {addr}")
        threading.Thread(target=handle_client, args=(client,)).start()


if __name__ == "__main__":
    threading.Thread(target=run_bottle).start()
    threading.Thread(target=run_proxy).start()