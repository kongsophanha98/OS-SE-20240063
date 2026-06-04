"""
Task 1: Bank Transfer - DEADLOCK VERSION
Two workers transfer money between accounts but lock in opposite order,
causing circular wait and deadlock.
"""

import threading
import time

# ── Accounts ────────────────────────────────────────────────────────────────
class Account:
    def __init__(self, name, balance):
        self.name = name
        self.balance = balance
        self.lock = threading.Semaphore(1)

account_a = Account("Account-A", 1000)
account_b = Account("Account-B", 1000)

transfer_done = [0]  # counts completed transfers
running = True

# ── Unsafe Transfer (causes deadlock) ───────────────────────────────────────
def transfer(from_acc, to_acc, amount, worker_name):
    print(f"{worker_name} trying to lock FROM {from_acc.name}")
    from_acc.lock.acquire()
    print(f"{worker_name} locked {from_acc.name} ✅")

    # Sleep to give other thread time to grab the other lock
    time.sleep(0.5)

    print(f"{worker_name} trying to lock TO {to_acc.name} ...")
    to_acc.lock.acquire()   # ← THIS IS WHERE DEADLOCK HAPPENS
    print(f"{worker_name} locked {to_acc.name} ✅")

    from_acc.balance -= amount
    to_acc.balance += amount
    print(f"{worker_name} ✅ Transfer complete: {amount} from {from_acc.name} to {to_acc.name}")

    to_acc.lock.release()
    from_acc.lock.release()
    transfer_done[0] += 1

# ── Watchdog ────────────────────────────────────────────────────────────────
def watchdog():
    time.sleep(3)  # wait 3 seconds
    if transfer_done[0] == 0:
        print("\n" + "="*50)
        print("💀 Deadlock detected: transactions are stuck")
        print("="*50)
        print(f"  Worker-1 is waiting for {account_b.name}")
        print(f"  Worker-2 is waiting for {account_a.name}")
        print(f"  Neither can proceed — circular wait!")
        print("="*50)
        print(f"\nCurrent balances (unchanged due to deadlock):")
        print(f"  {account_a.name}: {account_a.balance}")
        print(f"  {account_b.name}: {account_b.balance}")
        print(f"  Total: {account_a.balance + account_b.balance}")
        import os
        os._exit(1)

# ── Main ────────────────────────────────────────────────────────────────────
def main():
    print("=== Task 1: Bank Transfer WITHOUT Deadlock Prevention ===")
    print(f"Starting balances:")
    print(f"  {account_a.name}: {account_a.balance}")
    print(f"  {account_b.name}: {account_b.balance}")
    print(f"  Total: {account_a.balance + account_b.balance}")
    print()
    print("Worker-1: transfer 100 from Account-A to Account-B")
    print("Worker-2: transfer 200 from Account-B to Account-A")
    print()

    # Watchdog runs in background
    w = threading.Thread(target=watchdog, daemon=True)
    w.start()

    # Two workers locking in OPPOSITE order = deadlock
    t1 = threading.Thread(target=transfer,
                          args=(account_a, account_b, 100, "Worker-1"))
    t2 = threading.Thread(target=transfer,
                          args=(account_b, account_a, 200, "Worker-2"))

    t1.start()
    t2.start()
    t1.join()
    t2.join()

if __name__ == "__main__":
    main()
