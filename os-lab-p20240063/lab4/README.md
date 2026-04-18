# Lab 4 — I/O Redirection, Pipelines & Process Management

| | |
|---|---|
| **Student Name** | `Phanha` |
| **Student ID** | `p20240063` |

## Task Completion

| Task | Output File | Status |
|------|-----------|--------|
| Task 1: I/O Redirection | `task1_redirection.txt` | ✅ |
| Task 2: Pipelines & Filters | `task2_pipelines.txt` | ✅ |
| Task 3: Data Analysis | `task3_analysis.txt` | ✅ |
| Task 4: Process Management | `task4_processes.txt` | ✅ |
| Task 5: Orphan & Zombie | `task5_orphan_zombie.txt` | ✅ |

## Screenshots

### Task 4 — `top` Output
![top output](images/top_screenshot.png)

### Task 4 — `htop` Tree View
![htop tree](images/htop_tree_screenshot.png)

### Task 5 — Orphan Process (`ps` showing PPID = 1)
![orphan process](images/orphan_ps_output.png)

### Task 5 — Zombie Process (`ps` showing state Z)
![zombie process](images/zombie_ps_output.png)

### Task 4 — Top Memory Process
![top memory](images/top_memory_screenshot.png)

### Task 5 — Three Children Forest
![three children](images/three_children_forest.png)

### Terminal History
![history](images/history_screenshot.png)

## Answers to Task 5 Questions

1. **How are orphans cleaned up?**
   > Orphans are adopted by init/systemd (PID 1) which becomes their new parent and eventually reaps them.

2. **How are zombies cleaned up?**
   > Zombies are cleaned up when the parent calls wait() to read the child's exit status. If the parent exits, init/systemd adopts and reaps them.

3. **Can you kill a zombie with `kill -9`? Why or why not?**
   > No. A zombie is already dead — it has no running code. kill -9 only works on running processes. Only the parent calling wait() can remove a zombie from the process table.

## Reflection

> Pipelines and redirection are essential tools for real server work. Instead of scrolling through endless terminal output, we can filter, sort, and save exactly what we need. I found awk particularly powerful for log analysis. In a real server environment, I would use these techniques daily — for example, piping logs through grep and awk to find errors, redirecting output to log files, and using ps and kill to manage runaway processes.
