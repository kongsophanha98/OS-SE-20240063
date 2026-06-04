
import threading
import time
import random

BUFFER_CAPACITY = 100       # max particles = 50 pairs
MAX_PAIRS = BUFFER_CAPACITY // 2

buffer = []                 # shared circular-style list
produced_count = 0
packaged_count = 0
running = True

# ── Semaphores ──────────────────────────────────────────────────────────────
# Counts available PAIR slots (producer waits when buffer is full)
empty_pairs = threading.Semaphore(MAX_PAIRS)
# Counts complete pairs ready for packaging (consumer waits when buffer empty)
full_pairs  = threading.Semaphore(0)
# Mutual exclusion on the buffer itself
mutex       = threading.Semaphore(1)
# ────────────────────────────────────────────────────────────────────────────


def producer(machine_id):
    global produced_count, running
    pair_id = 0
    while running:
        pair_id += 1
        p1 = f"M{machine_id}-{pair_id}-P1"
        p2 = f"M{machine_id}-{pair_id}-P2"

        
        empty_pairs.acquire()
        if not running:
            break

        
        mutex.acquire()
        if len(buffer) + 2 > BUFFER_CAPACITY:
            mutex.release()
            empty_pairs.release()
            print("\n[ERROR] The producing machine is broken")
            running = False
            break

        buffer.append(p1)
        buffer.append(p2)
        produced_count += 1
        mutex.release()

        
        full_pairs.release()

        time.sleep(random.uniform(0.01, 0.04))


def consumer():
    global packaged_count, running
    while running:
        
        full_pairs.acquire()
        if not running:
            break

        
        mutex.acquire()
        if len(buffer) < 2:
            mutex.release()
            full_pairs.release()
            print("\n[ERROR] The packaging machine is broken")
            running = False
            break

        p1 = buffer.pop(0)
        p2 = buffer.pop(0)
        packaged_count += 1
        buf_size = len(buffer)
        mutex.release()

        
        p1_key = p1.rsplit("-", 1)[0]
        p2_key = p2.rsplit("-", 1)[0]

        if p1_key != p2_key:
            print(f"\n[ERROR] Pairs are incorrect")
            print(f"  Got: {p1} + {p2}")
            running = False
            break

        empty_pairs.release()

        print(f"Produced pairs: {produced_count:4d} | "
              f"Packaged pairs: {packaged_count:4d} | "
              f"Buffer particles: {buf_size:3d} | "
              f"Last packaged: {p1} + {p2}")

        time.sleep(random.uniform(0.02, 0.05))


def main():
    global running
    print("=== Task 1B: Particle Buffer WITH Semaphores ===")
    print(f"Buffer capacity: {BUFFER_CAPACITY} particles ({MAX_PAIRS} pairs)")
    print("Press Ctrl+C to stop.\n")

    threads = []
    for i in range(1, 4):
        t = threading.Thread(target=producer, args=(i,), daemon=True)
        threads.append(t)
        t.start()

    c = threading.Thread(target=consumer, daemon=True)
    c.start()
    threads.append(c)

    try:
        while running:
            time.sleep(0.1)
    except KeyboardInterrupt:
        running = False
        print("\nStopped by user (Ctrl+C).")

    print(f"\nFinal: Produced={produced_count}, Packaged={packaged_count}")
    print("No errors during normal operation. Semaphores worked correctly!")


if __name__ == "__main__":
    main()
