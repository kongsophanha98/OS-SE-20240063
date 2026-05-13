# Lab 5 — Threads, Kernel Workers & Process Signals

**Student ID:** p20240063
**Course:** Operating Systems

---

## Task 1 — Processes vs Threads
- `process_test.c`: Demonstrates that forked processes have separate memory.
  The child modifies `global_var` but the parent's copy stays unchanged.
- `thread_test.c`: Demonstrates that threads share memory.
  The spawned thread modifies `global_var` and the main thread sees the change.

## Task 2 — Thread Interaction
- `multi_thread.c`: Creates 3 worker threads, each returns a result via
  `pthread_exit`. Main thread collects results using `pthread_join`.

## Task 3 — Visualizing Kernel Threads
- `sleeper_threads.c`: Spawns 2 sleeping threads to demonstrate the 1:1
  thread model. Used `ps -eLf` and `/proc/<pid>/task/` to see LWP mapping.
- Used `htop` to visualize kernel worker threads like `[kworker/...]`.

## Task 4 — Process Signals
- `signal_handler.c`: Registers handlers for SIGINT and SIGTERM.
  Proves SIGKILL cannot be caught or ignored.

## Challenge
- `challenge.c`: Combines threads and signals. Two worker threads run
  in a loop. SIGINT sets `keep_running = 0`, causing threads to exit
  cleanly. Main thread joins both and prints goodbye message.

---

## Screenshots
| File | Description |
|------|-------------|
| process_vs_thread_1.png | process_test output |
| process_vs_thread_2.png | thread_test output |
| thread_interaction.png | multi_thread output |
| user_kernel_mapping.png | ps -eLf / proc mapping |
| htop_kernel_threads.png | htop kernel threads |
| signal_sigint.png | SIGKILL warning + Killed |
| challenge_shutdown.png | Challenge graceful shutdown |
