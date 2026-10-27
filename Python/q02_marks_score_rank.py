"""
Q2. Client - Server: Client enters marks, Server calculates
    Score (total + percentage), Pass/Fail and Rank.

HOW TO RUN (Windows):  python q02_marks_score_rank.py
Server and client run in this one file. Type the values when asked.
"""
import socket
import threading
import json   # used to send Python data (lists/dicts) as text over the socket

HOST, PORT = "127.0.0.1", 5002
PASS_MARK = 40                       # a student fails if ANY subject is below this
server_ready = threading.Event()


# ---------------------------- SERVER ----------------------------
def server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen(1)
    server_ready.set()
    conn, addr = s.accept()

    # receive: {"Alice": [80, 90, 70], "Bob": [30, 50, 60], ...}
    students = json.loads(conn.recv(4096).decode())

    results = []
    for name, marks in students.items():
        total = sum(marks)                         # Score = total marks
        percentage = total / len(marks)            # percentage = average mark
        status = "PASS" if min(marks) >= PASS_MARK else "FAIL"   # Pass / Fail
        results.append({"name": name, "total": total,
                        "percentage": round(percentage, 2),
                        "status": status})

    # Rank: sort by total (highest first); rank 1 = highest total
    results.sort(key=lambda r: r["total"], reverse=True)
    for position, r in enumerate(results, start=1):
        r["rank"] = position

    conn.send(json.dumps(results).encode())        # send result list back
    conn.close()
    s.close()


# ---------------------------- CLIENT ----------------------------
def client():
    server_ready.wait()
    c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    c.connect((HOST, PORT))

    n = int(input("Number of students : "))
    k = int(input("Number of subjects : "))
    students = {}
    for i in range(n):
        name = input(f"\nName of student {i + 1}: ")
        marks = [float(input(f"  Mark in subject {j + 1}: ")) for j in range(k)]
        students[name] = marks

    c.send(json.dumps(students).encode())          # send marks to server
    results = json.loads(c.recv(4096).decode())    # get calculated results
    c.close()

    print("\n{:<6}{:<12}{:>8}{:>8}{:>8}".format("Rank", "Name", "Total", "Avg%", "Result"))
    print("-" * 44)
    for r in results:
        print("{:<6}{:<12}{:>8}{:>8}{:>8}".format(
            r["rank"], r["name"], r["total"], r["percentage"], r["status"]))


if __name__ == "__main__":
    t = threading.Thread(target=server)
    t.start()
    client()
    t.join()
