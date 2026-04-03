# hub.py
import socket
import threading

clients = []

def handle_client(client_socket, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    clients.append(client_socket)
    while True:
        try:
            msg = client_socket.recv(1024).decode()
            if msg:
                print(f"[{addr}] {msg}")
                broadcast(msg, client_socket)
        except:
            print(f"[DISCONNECT] {addr} disconnected.")
            clients.remove(client_socket)
            client_socket.close()
            break

def broadcast(msg, sender):
    for client in clients:
        if client != sender:
            try:
                client.send(msg.encode())
            except:
                pass

def start_hub():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("127.0.0.1", 5555))
    server.listen()
    print("[HUB ACTIVE] Listening on 127.0.0.1:5555")
    while True:
        client, addr = server.accept()
        threading.Thread(target=handle_client, args=(client, addr), daemon=True).start()

if __name__ == "__main__":
    start_hub()
