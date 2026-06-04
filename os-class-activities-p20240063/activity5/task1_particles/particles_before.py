import threading
import time
import random

BUFFER_CAPACITY = 100  # max particles (50 pairs)
buffer = []
produced_count = 0
packaged_count = 0
running = True


buffer_lock = threading.Lock()

def producer(machine_id):
    global produced_count, running
    pair_id = 0
    while running:
        pair_id += 1
        p1 = f"M{machine_id}-{pair_id}-P1"
        p2 = f"M{machine_id}-{pair_id}-P2"

        
        if len(buffer) + 2 > BUFFER_CAPACITY:
            print("\n[ERROR] The producing machine is broken")
            running = False
            break

        with buffer_lock:
            buffer.append(p1)
        
        time.sleep(random.uniform(0, 0.002))  # simulate interleave window
        with buffer_lock:
            buffer.append(p2)
            produced_count += 1

        time.sleep(random.uniform(0.01, 0.05))

def consumer():
    global packaged_count, running
    while running:
        time.sleep(random.uniform(0.02, 0.06))

        with buffer_lock:
            if len(buffer) < 2:
                if len(buffer) == 0:
                    print("\n[ERROR] The packaging machine is broken")
                    running = False
                    break
                continue

            p1 = buffer.pop(0)
            p2 = buffer.pop(0)

        
        p1_parts = p1.rsplit("-", 1)   # ['M2-17', 'P1']
        p2_parts = p2.rsplit("-", 1)   # ['M2-17', 'P2']

        if p1_parts[0] != p2_parts[0]:
            print(f"\n[ERROR] Pairs are incorrect")
            print(f"  Got: {p1} + {p2}")
            running = False
            break

        with buffer_lock:
            packaged_count += 1

        print(f"Produced pairs: {produced_count} | Packaged pairs: {packaged_count} | "
              f"Buffer particles: {len(buffer)} | Last packaged: {p1} + {p2}")


def main():
    global running
    print("=== Task 1A: Particle Buffer WITHOUT Semaphores ===")
    print("Expect race conditions and incorrect pair errors!\n")

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
        print("\nStopped by user.")

    print(f"\nFinal: Produced={produced_count}, Packaged={packaged_count}")


if __name__ == "__main__":
    main()
