"""
Q1. Client - Server communication (TCP sockets)

HOW TO RUN (Windows, one window only):
    python q01_client_server.py
The server and the client both run inside this one file (server runs in a
background thread), so you do NOT need two terminals.
"""
import socket      # for network communication
import threading   # to run the server and client together in one file

HOST = "127.0.0.1"   # localhost (same computer)
PORT = 5001          # any free port number
server_ready = threading.Event()   # tells the client "server is listening now"


def server():
    # 1. create a TCP socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # allows quick re-run
    s.bind((HOST, PORT))          # 2. attach socket to address + port
    s.listen(1)                   # 3. wait for a client
    print("[SERVER] Waiting for client...")
    server_ready.set()            # tell client it can connect

    conn, addr = s.accept()       # 4. accept the connection
    print("[SERVER] Connected to", addr)

    data = conn.recv(1024).decode()          # 5. receive message from client
    print("[SERVER] Received:", data)

    reply = "Hello Client, I got your message: " + data
    conn.send(reply.encode())                # 6. send reply
    conn.close()
    s.close()


def client():
    server_ready.wait()                       # wait until server is listening
    c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    c.connect((HOST, PORT))                   # 1. connect to the server

    message = "Hello Server"
    c.send(message.encode())                  # 2. send message
    print("[CLIENT] Sent:", message)

    reply = c.recv(1024).decode()             # 3. receive reply
    print("[CLIENT] Received:", reply)
    c.close()


if __name__ == "__main__":
    t = threading.Thread(target=server)
    t.start()
    client()
    t.join()

# ---- If the exam asks for TWO separate files ----
# server.py  = the server() function + its imports, call server() at the end
# client.py  = the client() function + its imports (remove server_ready.wait())
# Run server.py first in one terminal, then client.py in a second terminal.
