"""
Q11. Task scheduler with 2 worker nodes - Round Robin assignment

 * Create several tasks with different processing times.
 * Assign tasks to the 2 workers in round-robin order:
        task1 -> Worker1, task2 -> Worker2, task3 -> Worker1, ...
 * Simulate execution: a worker runs its tasks one after another,
   so a task's completion time = (worker's busy time so far) + its own time.
 * Print completion time of each task and how many tasks each worker got.

HOW TO RUN (Windows):  python q11_task_scheduler_round_robin.py
"""

# (task name, processing time in seconds)
tasks = [
    ("Task1", 5),
    ("Task2", 3),
    ("Task3", 8),
    ("Task4", 2),
    ("Task5", 6),
    ("Task6", 4),
    ("Task7", 7),
]

workers = ["Worker1", "Worker2"]

# per-worker bookkeeping
available_at = {w: 0 for w in workers}     # time at which the worker becomes free
task_count = {w: 0 for w in workers}       # number of tasks assigned

print(f"{'Task':<8}{'Worker':<10}{'Proc.time':>10}{'Start':>8}{'Finish':>8}")
print("-" * 44)

for index, (name, proc_time) in enumerate(tasks):
    worker = workers[index % len(workers)]     # ROUND ROBIN: 0,1,0,1,0,1,...

    start = available_at[worker]               # starts when the worker is free
    finish = start + proc_time                 # completion time of this task
    available_at[worker] = finish              # worker is busy until 'finish'
    task_count[worker] += 1

    print(f"{name:<8}{worker:<10}{proc_time:>10}{start:>8}{finish:>8}")

print("\nNumber of tasks assigned to each worker:")
for w in workers:
    print(f"  {w}: {task_count[w]} tasks (busy until t = {available_at[w]})")

print("\nAll tasks completed at t =", max(available_at.values()))
