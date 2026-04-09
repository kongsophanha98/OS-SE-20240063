# Activity 2 — Processes & IPC

## Student: Phanha  
## Course: OS Class  
## Activity: Task 1–4  

---

## Task 1 — forkchild.c (Process Creation in WSL/Linux)

- Created a child process using `fork()`.
- Parent and child print their PIDs.
- **Output** saved in `result_forkchild.txt`.

**Notes:**
- Parent waits for child to finish using `wait()`.
- Shows basic process creation.

---

## Task 2 — winprocess.c (Windows Process Creation)

- Created a child process to run **MS Paint** using `CreateProcess()`.
- Parent PID and child PID printed.
- **Screenshots** saved in `screenshots/`:
  - `task2_taskmanager_tree.png`
  - `task2_taskmanager_details.png`

**Notes:**
- Windows Store apps like Paint may not nest under parent process in Task Manager.
- Full path to `mspaint.exe` must be used.

---

## Task 3 — Shared Memory IPC

- **Producer** writes data to shared memory.
- **Consumer** reads from shared memory.
- **Execution order matters:** producer must run before consumer.
- **Files:**  
  - Producer: `shm-producer.c`  
  - Consumer: `shm-consumer.c`  
  - Common header: `common.h`
- **Output saved in:** `result-shm-ipc.txt`

**Notes:**
- Shared memory acts like a “whiteboard” in RAM.
- Data must exist before consumer reads it.
- Demonstrates fast, direct memory communication between processes.

---

## Task 4 — Message Queue IPC

- **Sender** sends message to POSIX message queue.
- **Receiver** reads the message.
- **Execution order:** sender must run before receiver (queue must exist).
- **Files:**  
  - Sender: `sender.c`  
  - Receiver: `receiver.c`  
  - Common header: `common.h`
- **Output saved in:** `result-mq-ipc.txt`

**Notes:**
- Message queue acts like a “mailbox” between processes.
- Unlike shared memory, processes do not share memory directly.
- Receiver prints: `"Hello from sender! This is message queue IPC."`

---

## Screenshots & Outputs

- All screenshots are in `activity2/screenshots/`
- All program outputs saved in `.txt` files for submission.

---

## Execution Instructions

1. **Task 1:**  
   ```bash
   gcc -o forkchild forkchild.c
   ./forkchild

Task 2 (Windows):

Open PowerShell
gcc -o winprocess winprocess.c
.\winprocess.exe
Take Task Manager screenshots

Task 3 (Shared Memory IPC):
Open two terminals in task3_shm
Terminal 1: ./shm-producer
Terminal 2: ./shm-consumer

Task 4 (Message Queue IPC):
Open two terminals in task4_mq
Terminal 1: ./sender
Terminal 2: ./receiver
