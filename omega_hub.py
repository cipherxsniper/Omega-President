import socket
import threading

clients = []

def handle_client(conn, addr):
    print(f"[CONNECTED] {addr}")
    while True:
        try:
            msg = conn.recv(1024).decode()
            if not msg:
                break
            # broadcast to other nodes
            for c in clients:
                if c != conn:
                    c.send(msg.encode())
        except:
            break
    clients.remove(conn)
    conn.close()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('127.0.0.1', 5555))
server.listen()
print("[HUB ACTIVE] Listening on 127.0.0.1:5555")

while True:
    conn, addr = server.accept()
    clients.append(conn)
    threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()
