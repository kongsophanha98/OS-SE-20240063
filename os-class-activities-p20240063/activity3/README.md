# Class Activity 3 — Socket Communication & Multithreading

- **Student Name:** Phanha
- **Student ID:** p20240063
- **Date:** April 2026

---

## Task 1: TCP Socket Communication (C)

### Compilation & Execution

```bash
gcc -o server server.c
gcc -o client client.c
./server &
sleep 1
./client
```

**Server Output:**
```
Server: socket created (fd=3)
Server: bound to port 8080
Server: listening... waiting for a client to connect.
Server: client connected!
Server: received from client: "Hello from client!"
Server: sent response: "Hello from server!"
Server: connection closed.
```

**Client Output:**
```
Client: socket created
Client: connecting to server on port 8080...
Client: connected!
Client: sent message: "Hello from client!"
Client: received from server: "Hello from server!"
Client: connection closed.
```

![Socket exchange](screenshots/task1_socket_exchange.png)

### Answers

1. **Role of `bind()` / Why client doesn't call it:**
   > `bind()` assigns the server a specific IP address and port number to listen on, so clients know where to connect. The client doesn't call `bind()` because the OS automatically assigns it a random available port — the client only needs to know the server's address, not its own.

2. **What `accept()` returns:**
   > `accept()` returns a **new** socket file descriptor dedicated to communicating with the connected client. It is different from the original server socket — the original socket keeps listening for new connections, while the new one is used only for sending/receiving data with that specific client.

3. **Starting client before server:**
   > You get a `Connection refused` error because no process is listening on port 8080 yet. The client's `connect()` call fails immediately since there is no server to accept the connection.

4. **What `htons()` does:**
   > `htons()` (Host TO Network Short) converts a port number from the host's byte order to network byte order (big-endian). This is needed because different CPU architectures store multi-byte numbers differently (little-endian vs big-endian), and the network protocol requires a standard byte order.

5. **Socket call sequence diagram:**
   ```
   Server:  socket() → bind() → listen() → accept() → recv() → send() → close()
   Client:  socket()                     → connect() → send() → recv() → close()
   ```

---

## Task 2: POSIX Threads (C)

### Output — Without Mutex (Race Condition)

```
Main thread (TID: 128509460924224): creating 4 threads...
PID: 2114 — use this to observe threads with ps or htop

Thread 2 (TID: 128509450118848): starting work...
Thread 4 (TID: 128509433333440): starting work...
Thread 1 (TID: 128509458511552): starting work...
Thread 3 (TID: 128509441726144): starting work...
Thread 4 (TID: 128509433333440): done.
Thread 1 (TID: 128509458511552): done.
Thread 2 (TID: 128509450118848): done.
Thread 3 (TID: 128509441726144): done.

All threads completed.
Expected counter value: 400000
Actual counter value:   186217
⚠️  Race condition detected! Counter is incorrect.
```

### Output — With Mutex (Correct)

```
Main thread (TID: 133200523822912): creating 4 threads (with mutex)...
Thread 1 (TID: 133200521197248): starting work...
Thread 3 (TID: 133200504411840): starting work...
Thread 2 (TID: 133200512804544): starting work...
Thread 4 (TID: 133200496019136): starting work...
Thread 3 (TID: 133200504411840): done.
Thread 4 (TID: 133200496019136): done.
Thread 1 (TID: 133200521197248): done.
Thread 2 (TID: 133200512804544): done.

All threads completed.
Expected counter value: 400000
Actual counter value:   400000
✅ Counter is correct! Mutex prevented the race condition.
```

![Threads output](screenshots/task2_threads_output.png)

### Answers

1. **What is a race condition?**
   > A race condition occurs when multiple threads access and modify shared data simultaneously, and the final result depends on the timing/order of execution. In `threads.c`, multiple threads read `shared_counter`, increment it, and write it back — but another thread may have already changed it in between, causing increments to be lost. That's why the counter never reaches 400000.

2. **What does `pthread_mutex_lock()` do?**
   > `pthread_mutex_lock()` ensures only one thread can enter the protected code block at a time. When one thread holds the lock, all other threads trying to lock it will block and wait. This makes the read-increment-write operation atomic, so no updates are lost and the counter is always correct.

3. **Removing `pthread_join()`:**
   > Without `pthread_join()`, the main thread exits immediately after creating the worker threads, which terminates the entire process. The worker threads are killed before they finish their work, resulting in an incomplete or zero counter value.

4. **Thread vs Process:**
   > Threads **share**: code segment, heap memory, global variables, open file descriptors, and signal handlers. Each thread has **private**: its own stack, registers, thread ID, and program counter. Processes have completely separate memory spaces and must use IPC to communicate, while threads communicate through shared memory directly.

---

## Task 3: Java Multithreading

### ThreadDemo Output

```
Main thread (ID: 1): starting...
PID: 3714 — observe threads with ps or htop

[Alpha] Count: 1 (Thread ID: 20)
[Beta] Count: 1 (Thread ID: 21)
[Gamma] Count: 1 (Thread ID: 22)
[Beta] Count: 2 (Thread ID: 21)
[Gamma] Count: 2 (Thread ID: 22)
[Alpha] Count: 2 (Thread ID: 20)
...
[Beta] Finished!
[Gamma] Finished!
[Alpha] Finished!

Main thread: all threads finished.
```

### RunnableDemo Output

```
Main: creating threads with Runnable interface

[Download] Step 1 (Thread: downloader, ID: 20)
[Process] Step 1 (Thread: processor, ID: 21)
[Upload] Step 1 (Thread: uploader, ID: 22)
[Download] Step 2 (Thread: downloader, ID: 20)
[Upload] Step 2 (Thread: uploader, ID: 22)
[Process] Step 2 (Thread: processor, ID: 21)
...
Main: all tasks completed.
```

### PoolDemo Output

```
Main: creating thread pool with 2 threads for 6 tasks

Task 2 started on thread pool-1-thread-2 (ID: 21)
Task 1 started on thread pool-1-thread-1 (ID: 20)
Task 1 completed on thread pool-1-thread-1
Task 2 completed on thread pool-1-thread-2
Task 4 started on thread pool-1-thread-2 (ID: 21)
Task 3 started on thread pool-1-thread-1 (ID: 20)
...
Main: all tasks completed. Pool shut down.
```

![Java threading](screenshots/task3_java_output.png)

### Answers

1. **Thread vs Runnable:**
   > `extends Thread` creates a subclass of Thread and overrides `run()` — it's simpler but limits flexibility since Java only allows single inheritance. `implements Runnable` separates the task logic from thread management and is preferred because your class can still extend another class. Runnable is the better choice in most cases, especially when using thread pools.

2. **Pool size limiting concurrency:**
   > The pool was created with `Executors.newFixedThreadPool(2)`, meaning only 2 threads exist in the pool. When 6 tasks are submitted, only 2 run simultaneously — the other 4 wait in a queue until a thread becomes free. This is confirmed by the output showing only `pool-1-thread-1` and `pool-1-thread-2` ever running.

3. **`thread.join()` in Java:**
   > `thread.join()` makes the calling thread (main) wait until the specified thread finishes execution. Without it in `ThreadDemo`, the main thread would print "all threads finished" immediately and potentially exit before Alpha, Beta, and Gamma complete their counting.

4. **ExecutorService advantages:**
   > `ExecutorService` is better because it reuses threads from a pool (no overhead of creating/destroying threads for each task), automatically manages a task queue, handles thread lifecycle cleanly with `shutdown()`, supports futures and return values, and scales much better for large applications with many concurrent tasks.

---

## Task 4: Observing Threads

### Linux — `ps -eLf` Output

```
phanha  3992  365  3992  0  5  23:39  pts/0  00:00:00  ./threads_observe
phanha  3992  365  3995  0  5  23:39  pts/0  00:00:00  ./threads_observe
phanha  3992  365  3996  0  5  23:39  pts/0  00:00:00  ./threads_observe
phanha  3992  365  3997  0  5  23:39  pts/0  00:00:00  ./threads_observe
phanha  3992  365  3998  0  5  23:39  pts/0  00:00:00  ./threads_observe
```

### Linux — `/proc/PID/task/` listing

```
3992  3995  3996  3997  3998
Total: 5
```

### Linux — htop Thread View

![htop threads](screenshots/task4_htop_threads.png)

### Windows — Task Manager

![Task Manager threads](screenshots/task4_taskmanager_threads.png)

### Answers

1. **LWP column meaning:**
   > LWP stands for **Light Weight Process** — it is the kernel-level thread ID assigned to each thread. All threads in the same process share the same PID, but each has a unique LWP. In the output, PID 3992 has 5 LWP values (3992, 3995, 3996, 3997, 3998) representing the main thread and 4 worker threads.

2. **`/proc/PID/task/` count:**
   > There were **5 entries** in `/proc/3992/task/` — matching exactly 1 main thread + 4 worker threads created by `pthread_create()`. This confirms that the Linux kernel creates a separate task entry for every thread.

3. **Extra Java threads:**
   > `java.exe` shows more threads than the 3 created in code because the JVM automatically creates internal threads for garbage collection, JIT (Just-In-Time) compilation, signal handling, finalizer, and other runtime services. These background threads are invisible to the programmer but visible at the OS level.

4. **Linux vs Windows thread viewing:**
   > Linux tools (`ps -eLf`, `/proc/PID/task/`, `htop`) provide much more detail — you can see individual thread IDs (LWP), CPU time per thread, and thread states. Windows Task Manager only shows a total thread **count** per process, without individual thread details. For detailed thread inspection on Windows, tools like Process Explorer or `jstack` are needed.

---

## Reflection

> Working through this activity gave me a much clearer picture of how processes communicate and how threads work at the OS level. The socket task showed how two completely separate processes can exchange data over a network connection using a structured sequence of system calls. Seeing the server block on `accept()` until a client connects made the client-server model very tangible.
>
> The threading tasks were the most eye-opening — especially observing the race condition in action. Running `threads.c` multiple times and getting a different wrong answer each time made the concept of non-deterministic behavior very real. The mutex fix was satisfying to see work perfectly every time.
>
> Using `ps`, `/proc`, and `htop` to observe threads at the kernel level connected the high-level programming concepts to what the OS actually does. Knowing that each thread has its own LWP and appears as a separate entry in `/proc` helps explain why thread management has real overhead, and why tools like `ExecutorService` that reuse threads are important for performance.
