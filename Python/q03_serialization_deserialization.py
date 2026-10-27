"""
Q3. Client - Server communication with Serialization and Deserialization

Serialization   = converting a Python object (dict/list/class) into bytes
                  so it can travel over the network  (pickle.dumps)
Deserialization = converting those bytes back into the Python object
                  (pickle.loads)

HOW TO RUN (Windows):  python q03_serialization_deserialization.py
"""
import socket
import threading
import pickle    # Python's built-in serialization module

HOST, PORT = "127.0.0.1", 5003
server_ready = threading.Event()


def server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen(1)
    server_ready.set()
    conn, addr = s.accept()

    raw_bytes = conn.recv(4096)
    data = pickle.loads(raw_bytes)               # DESERIALIZE: bytes -> dict
    print("[SERVER] Received (after deserialization):", data)

    # change the object: add a new field and double the marks
    data["marks"] = [m * 2 for m in data["marks"]]
    data["processed_by"] = "server"

    conn.send(pickle.dumps(data))                # SERIALIZE: dict -> bytes
    conn.close()
    s.close()


def client():
    server_ready.wait()
    c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    c.connect((HOST, PORT))

    student = {"name": "Medha", "roll": 101, "marks": [80, 90, 85]}
    print("[CLIENT] Original object        :", student)

    serialized = pickle.dumps(student)           # SERIALIZE: dict -> bytes
    print("[CLIENT] Serialized (raw bytes) :", serialized[:40], "...")
    c.send(serialized)

    reply = pickle.loads(c.recv(4096))           # DESERIALIZE the reply
    print("[CLIENT] Reply (deserialized)   :", reply)
    c.close()


if __name__ == "__main__":
    t = threading.Thread(target=server)
    t.start()
    client()
    t.join()
