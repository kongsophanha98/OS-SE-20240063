#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/mman.h>
#include <sys/stat.h>
#include <sys/wait.h>

#define SHM_NAME "/my_shm"
#define SIZE 4096

int main() {
    int fd;
    char *ptr;

    // Create shared memory object
    fd = shm_open(SHM_NAME, O_CREAT | O_RDWR, 0666);
    if (fd == -1) {
        perror("shm_open");
        exit(1);
    }

    // Set size
    ftruncate(fd, SIZE);

    // Map memory
    ptr = mmap(0, SIZE, PROT_READ | PROT_WRITE, MAP_SHARED, fd, 0);
    if (ptr == MAP_FAILED) {
        perror("mmap");
        exit(1);
    }

    pid_t pid = fork();

    if (pid < 0) {
        perror("fork");
        exit(1);
    }

    if (pid == 0) {
        // Child = Consumer
        sleep(2);
        printf("Child reading from shared memory: %s\n", ptr);
    } else {
        // Parent = Producer
        strcpy(ptr, "Hello from shared memory!");
        printf("Parent wrote to shared memory.\n");

        wait(NULL);
    }

    // Cleanup
    munmap(ptr, SIZE);
    close(fd);
    shm_unlink(SHM_NAME);

    return 0;
}
