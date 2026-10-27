"""
Q7. Berkeley's Algorithm (clock synchronisation)

Idea:
 1. The MASTER (time daemon) asks every slave for its current clock time.
 2. Master finds the difference of each slave's clock from its own clock.
 3. Master takes the AVERAGE of all differences (including its own = 0).
 4. Master tells every machine how much to ADJUST its clock
    (adjustment = average - that machine's own difference).
 After this, all clocks show the same time.

HOW TO RUN (Windows):  python q07_berkeley_algorithm.py
(This is a simulation - clocks are given in minutes, as in textbook examples.)
"""


def to_minutes(hhmm):
    """'3:25' -> 205 minutes since midnight"""
    h, m = hhmm.split(":")
    return int(h) * 60 + int(m)


def to_hhmm(minutes):
    """205 -> '3:25'"""
    return f"{int(minutes // 60) % 24}:{int(minutes % 60):02d}"


def berkeley(clocks):
    """
    clocks : dict  {machine name: time in minutes}. First entry = MASTER.
    returns: dict of synchronised times
    """
    names = list(clocks)
    master = names[0]
    master_time = clocks[master]

    print(f"MASTER is {master}, its time = {to_hhmm(master_time)}\n")

    # Step 1 & 2: master polls slaves and computes difference from its own time
    differences = {}
    for name in names:
        differences[name] = clocks[name] - master_time      # master's own diff = 0
        print(f"{name:<8} clock = {to_hhmm(clocks[name]):>6}   "
              f"difference from master = {differences[name]:+d} min")

    # Step 3: average of all differences
    average_diff = sum(differences.values()) / len(differences)
    print(f"\nAverage difference = {average_diff:+.2f} min")

    # Step 4: adjustment for each machine and the new time
    synced = {}
    print("\nAdjustments sent by master:")
    for name in names:
        adjustment = average_diff - differences[name]
        synced[name] = clocks[name] + adjustment
        print(f"{name:<8} adjust by {adjustment:+.2f} min  ->  new time = {to_hhmm(synced[name])}")
    return synced


if __name__ == "__main__":
    # Classic textbook example: master 3:00, slave1 3:25, slave2 2:50
    clocks = {
        "Master": to_minutes("3:00"),
        "Slave1": to_minutes("3:25"),
        "Slave2": to_minutes("2:50"),
    }
    final = berkeley(clocks)
    print("\nAll clocks after synchronisation:",
          {k: to_hhmm(v) for k, v in final.items()})
