#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/wait.h>

int main() {
    pid_t pid = fork();

    if (pid == 0) {
        printf("Child (PID %d): Exiting now.\n", getpid());
        exit(0);
    }

    printf("Parent (PID %d): Child PID is %d. Sleeping 10 seconds...\n", getpid(), pid);
    sleep(10);
    wait(NULL);
    printf("Parent: Called wait() - zombie cleaned up!\n");
    sleep(5);
    return 0;
}
