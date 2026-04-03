import socket
import threading

clients = []

def handle_client(conn):
    while True:
        try:
            msg = conn.recv(1024)
            if msg:
                for c in clients:
                    if c != conn:
                        c.send(msg)
        except:
            if conn in clients:
                clients.remove(conn)
            conn.close()
            break

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('127.0.0.1', 5555))  # Hub IP + Port
server.listen()
print("[HUB] Listening on 127.0.0.1:5555")

while True:
    conn, addr = server.accept()
    clients.append(conn)
    threading.Thread(target=handle_client, args=(conn,), daemon=True).start()
