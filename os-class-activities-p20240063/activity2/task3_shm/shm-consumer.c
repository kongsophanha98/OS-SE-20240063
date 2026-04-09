#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <sys/mman.h>
#include <sys/stat.h>
#include <unistd.h>

int main() {
    const int SIZE = 4096;
    const char *name = "OS-phanha";        // ← SAME NAME

    int shm_fd = shm_open(name, O_RDONLY, 0666);
    void *ptr = mmap(0, SIZE, PROT_READ, MAP_SHARED, shm_fd, 0);

    printf("Consumer: reading from shared memory '%s'\n", name);
    printf("Consumer: message = \"%s\"\n", (char *)ptr);

    shm_unlink(name);
    return 0;
}
