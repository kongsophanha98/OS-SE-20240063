#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <mqueue.h>
#include <unistd.h>
#include <sys/wait.h>

#define QUEUE_NAME "/my_queue"
#define MAX_SIZE 1024

int main() {
    mqd_t mq;
    struct mq_attr attr;

    attr.mq_flags = 0;
    attr.mq_maxmsg = 10;
    attr.mq_msgsize = MAX_SIZE;
    attr.mq_curmsgs = 0;

    mq = mq_open(QUEUE_NAME, O_CREAT | O_RDWR, 0666, &attr);
    if (mq == (mqd_t)-1) {
        perror("mq_open");
        exit(1);
    }

    pid_t pid = fork();

    if (pid < 0) {
        perror("fork");
        exit(1);
    }

    if (pid == 0) {
        // Child = receiver
        char buffer[MAX_SIZE];
        sleep(2);

        if (mq_receive(mq, buffer, MAX_SIZE, NULL) == -1) {
            perror("mq_receive");
            exit(1);
        }

        printf("Child received message: %s\n", buffer);
    } else {
        // Parent = sender
        char message[] = "Hello from message queue!";
        
        if (mq_send(mq, message, strlen(message) + 1, 0) == -1) {
            perror("mq_send");
            exit(1);
        }

        printf("Parent sent message.\n");

        wait(NULL);
    }

    mq_close(mq);
    mq_unlink(QUEUE_NAME);

    return 0;
}
