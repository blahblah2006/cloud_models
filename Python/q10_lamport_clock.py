"""
Q10. Implementation of Lamport Logical Clock

Rules:
 1. Before every local event, a process increments its clock:  C = C + 1
 2. When sending a message, the process increments its clock and
    attaches the clock value (timestamp) to the message.
 3. When receiving a message with timestamp T:
        C = max(C, T) + 1

HOW TO RUN (Windows):  python q10_lamport_clock.py
"""


class Process:
    def __init__(self, name):
        self.name = name
        self.clock = 0                       # Lamport clock starts at 0

    def local_event(self, description):
        self.clock += 1                      # rule 1
        print(f"{self.name}: local event '{description}'  -> clock = {self.clock}")

    def send(self, receiver, message):
        self.clock += 1                      # rule 2: increment before sending
        timestamp = self.clock
        print(f"{self.name}: SENDS '{message}' to {receiver.name} "
              f"with timestamp {timestamp}  -> clock = {self.clock}")
        receiver.receive(self, message, timestamp)

    def receive(self, sender, message, timestamp):
        old = self.clock
        self.clock = max(self.clock, timestamp) + 1      # rule 3
        print(f"{self.name}: RECEIVES '{message}' from {sender.name} "
              f"(ts={timestamp}) -> clock = max({old},{timestamp})+1 = {self.clock}")


if __name__ == "__main__":
    p1, p2, p3 = Process("P1"), Process("P2"), Process("P3")

    p1.local_event("a")
    p1.send(p2, "m1")          # P1 -> P2
    p2.local_event("b")
    p2.send(p3, "m2")          # P2 -> P3
    p3.local_event("c")
    p3.send(p1, "m3")          # P3 -> P1
    p1.local_event("d")

    print("\nFinal Lamport clocks:",
          f"P1={p1.clock}, P2={p2.clock}, P3={p3.clock}")
