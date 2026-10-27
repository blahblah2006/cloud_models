"""
Q8. Clock drift simulation

Clock A and Clock B start at the same time.
Clock B runs FASTER by 10 milliseconds every second.
Simulate for 1 minute (60 seconds) and find how far apart they become.

Expected answer: 60 s x 10 ms = 600 ms (0.6 s) difference.

HOW TO RUN (Windows):  python q08_clock_drift.py
(Simulated - it does NOT wait 60 real seconds.)
"""

DRIFT_PER_SECOND_MS = 10     # clock B gains 10 ms every real second
DURATION_SECONDS = 60        # simulate 1 minute

# both clocks start at the same time (0 ms)
clock_a_ms = 0.0
clock_b_ms = 0.0

print(f"{'Real time (s)':>14} {'Clock A (ms)':>14} {'Clock B (ms)':>14} {'Difference (ms)':>16}")
print("-" * 62)

for second in range(1, DURATION_SECONDS + 1):
    clock_a_ms += 1000                              # A: exactly 1000 ms per second
    clock_b_ms += 1000 + DRIFT_PER_SECOND_MS        # B: 1010 ms per second (runs fast)
    difference = clock_b_ms - clock_a_ms            # how far apart now

    # print every 10 seconds (and the final second)
    if second % 10 == 0 or second == DURATION_SECONDS:
        print(f"{second:>14} {clock_a_ms:>14.0f} {clock_b_ms:>14.0f} {difference:>16.0f}")

print("\nAfter 1 minute the clocks differ by",
      f"{difference:.0f} ms ({difference / 1000} seconds).")
