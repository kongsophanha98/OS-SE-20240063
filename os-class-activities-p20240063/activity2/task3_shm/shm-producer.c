#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <fcntl.h>
#include <sys/mman.h>
#include <sys/stat.h>
#include <unistd.h>

int main() {
    const int SIZE = 4096;
    const char *name = "OS-phanha";        // ← YOUR UNIQUE NAME
    const char *message_0 = "Hello, ";
    const char *message_1 = "this is shared memory IPC!";

    int shm_fd = shm_open(name, O_CREAT | O_RDWR, 0666);
    ftruncate(shm_fd, SIZE);
    void *ptr = mmap(0, SIZE, PROT_WRITE, MAP_SHARED, shm_fd, 0);

    sprintf(ptr, "%s", message_0);
    ptr += strlen(message_0);
    sprintf(ptr, "%s", message_1);

    printf("Producer: wrote to shared memory '%s'\n", name);
    return 0;
}
