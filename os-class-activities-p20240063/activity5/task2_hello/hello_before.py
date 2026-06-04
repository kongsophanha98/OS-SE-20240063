import threading
import time
import random
import sys

output = []
lock = threading.Lock()

def process1():
    time.sleep(random.uniform(0, 0.05))
    with lock:
        output.append('H')
        sys.stdout.write('H')
        sys.stdout.flush()
    time.sleep(random.uniform(0, 0.05))
    with lock:
        output.append('E')
        sys.stdout.write('E')
        sys.stdout.flush()

def process2():
    time.sleep(random.uniform(0, 0.05))
    with lock:
        output.append('L')
        sys.stdout.write('L')
        sys.stdout.flush()
    time.sleep(random.uniform(0, 0.05))
    with lock:
        output.append('L')
        sys.stdout.write('L')
        sys.stdout.flush()

def process3():
    time.sleep(random.uniform(0, 0.05))
    with lock:
        output.append('O')
        sys.stdout.write('O')
        sys.stdout.flush()


def main():
    print("=== Task 2A: Print HELLO WITHOUT Semaphores ===")
    print("Running 5 trials to show unpredictable ordering:\n")

    for trial in range(1, 6):
        output.clear()
        sys.stdout.write(f"Trial {trial}: ")
        sys.stdout.flush()

        t1 = threading.Thread(target=process1)
        t2 = threading.Thread(target=process2)
        t3 = threading.Thread(target=process3)

        t1.start(); t2.start(); t3.start()
        t1.join();  t2.join();  t3.join()

        result = ''.join(output)
        correct = result == "HELLO"
        print(f"  <- {'CORRECT' if correct else 'WRONG! Expected HELLO'}")

    print("\nConclusion: Without semaphores, output order is non-deterministic.")
    print("The threads race and letters appear in whatever order the OS schedules them.")


if __name__ == "__main__":
    main()
