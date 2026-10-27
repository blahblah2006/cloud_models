"""
Q5. Token Ring Algorithm (Mutual Exclusion)

Multiple processes are arranged in a circle. ONE token goes round the ring.
A process may enter the Critical Section (CS) ONLY when it holds the token.
After using (or skipping) the CS it passes the token to the next process.

HOW TO RUN (Windows):  python q05_token_ring.py
"""
import multiprocessing as mp   # real separate processes
import time
import random

NUM_PROCESSES = 5   # processes in the ring
ROUNDS = 2          # how many times the token goes around the full ring


def process(pid, my_queue, next_queue, done_event):
    """
    pid        : id of this process (0..N-1)
    my_queue   : queue from which this process RECEIVES the token
    next_queue : queue of the next process in the ring (token is SENT here)
    """
    for _ in range(ROUNDS):
        token = my_queue.get()                 # wait here until token arrives
        print(f"Process {pid} received the TOKEN")

        # Process decides randomly whether it wants the critical section
        if random.choice([True, False]):
            print(f"   >>> Process {pid} ENTERS critical section")
            time.sleep(0.5)                    # simulate work in the CS
            print(f"   <<< Process {pid} LEAVES critical section")
        else:
            print(f"   Process {pid} does not need the critical section")

        next_queue.put(token)                  # pass the token to next process
    done_event.set()


if __name__ == "__main__":
    # one queue per process = the "link" that feeds that process
    queues = [mp.Queue() for _ in range(NUM_PROCESSES)]
    events = [mp.Event() for _ in range(NUM_PROCESSES)]

    procs = []
    for i in range(NUM_PROCESSES):
        nxt = (i + 1) % NUM_PROCESSES          # circular: last -> first
        p = mp.Process(target=process, args=(i, queues[i], queues[nxt], events[i]))
        procs.append(p)
        p.start()

    queues[0].put("TOKEN")                     # give the token to process 0 first

    for p in procs:
        p.join()
    print("\nToken ring simulation finished.")
