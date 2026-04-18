#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/wait.h>

int main() {
    int i;
    for(i = 0; i < 3; i++) {
        pid_t pid = fork();
        if (pid == 0) {
            printf("Child %d (PID %d): Sleeping...\n", i+1, getpid());
            sleep(30);
            exit(0);
        }
    }
    printf("Parent (PID %d): Waiting for 3 children...\n", getpid());
    sleep(30);
    wait(NULL);
    wait(NULL);
    wait(NULL);
    return 0;
}
