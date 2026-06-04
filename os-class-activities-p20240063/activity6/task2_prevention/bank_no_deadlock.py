"""
Task 2: Bank Transfer - DEADLOCK PREVENTION VERSION
Uses one shared mutex semaphore (initialized to 1) to protect
the entire transfer operation. Only one transfer runs at a time.
No circular wait is possible.
"""

import threading
import time

# ── Accounts ────────────────────────────────────────────────────────────────
class Account:
    def __init__(self, name, balance):
        self.name = name
        self.balance = balance

account_a = Account("Account-A", 1000)
account_b = Account("Account-B", 1000)

# ── ONE shared mutex protects ALL transfers ──────────────────────────────────
mutex = threading.Semaphore(1)

# ── Safe Transfer ────────────────────────────────────────────────────────────
def transfer(from_acc, to_acc, amount, worker_name):
    print(f"{worker_name} waiting for mutex...")
    mutex.acquire()
    try:
        print(f"{worker_name} acquired mutex ✅")
        time.sleep(0.2)  # simulate processing time

        from_acc.balance -= amount
        to_acc.balance += amount

        print(f"{worker_name} ✅ Transferred {amount} from {from_acc.name} to {to_acc.name}")
        print(f"  {account_a.name}: {account_a.balance} | {account_b.name}: {account_b.balance}")
    finally:
        mutex.release()
        print(f"{worker_name} released mutex")

# ── Main ────────────────────────────────────────────────────────────────────
def main():
    print("=== Task 2: Bank Transfer WITH Deadlock Prevention ===")
    print(f"Strategy: Single shared mutex semaphore (initialized to 1)")
    print()
    print(f"Starting balances:")
    print(f"  {account_a.name}: {account_a.balance}")
    print(f"  {account_b.name}: {account_b.balance}")
    starting_total = account_a.balance + account_b.balance
    print(f"  Starting total: {starting_total}")
    print()
    print("Worker-1: transfer 100 from Account-A to Account-B")
    print("Worker-2: transfer 200 from Account-B to Account-A")
    print()

    t1 = threading.Thread(target=transfer,
                          args=(account_a, account_b, 100, "Worker-1"))
    t2 = threading.Thread(target=transfer,
                          args=(account_b, account_a, 200, "Worker-2"))

    t1.start()
    t2.start()
    t1.join()
    t2.join()

    final_total = account_a.balance + account_b.balance
    print()
    print("="*50)
    print(f"Final balances:")
    print(f"  {account_a.name}: {account_a.balance}")
    print(f"  {account_b.name}: {account_b.balance}")
    print(f"  Final total: {final_total}")
    print()
    if final_total == starting_total:
        print("✅ Total balance preserved — no money lost!")
    else:
        print("❌ ERROR: Total balance mismatch!")
    print("✅ No deadlock occurred")
    print("="*50)

if __name__ == "__main__":
    main()
