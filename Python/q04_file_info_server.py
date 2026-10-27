"""
Q4. Client sends a filename; Server looks for that file and returns
    the number of lines, words and the size of the file to the client.

HOW TO RUN (Windows):  python q04_file_info_server.py
Type a file name when asked. A sample file 'sample.txt' is created
automatically so you can type:  sample.txt
"""
import os
import socket
import threading

HOST, PORT = "127.0.0.1", 5004
server_ready = threading.Event()


def server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen(1)
    server_ready.set()
    conn, addr = s.accept()

    filename = conn.recv(1024).decode()           # filename sent by client
    print("[SERVER] Client asked for file:", filename)

    if os.path.exists(filename):                  # does the file exist?
        with open(filename, "r") as f:
            text = f.read()
        lines = len(text.splitlines())            # number of lines
        words = len(text.split())                 # number of words
        size = os.path.getsize(filename)          # size in bytes
        reply = f"Lines = {lines}, Words = {words}, Size = {size} bytes"
    else:
        reply = "ERROR: File not found"

    conn.send(reply.encode())
    conn.close()
    s.close()


def client():
    server_ready.wait()
    c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    c.connect((HOST, PORT))

    filename = input("Enter file name: ")
    c.send(filename.encode())
    print("[CLIENT] Server says ->", c.recv(1024).decode())
    c.close()


if __name__ == "__main__":
    # create a sample file so the program can be tested immediately
    if not os.path.exists("sample.txt"):
        with open("sample.txt", "w") as f:
            f.write("Cloud computing is great\nDistributed systems are fun\nPython sockets work well\n")

    t = threading.Thread(target=server)
    t.start()
    client()
    t.join()
