#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <mqueue.h>
#include <fcntl.h>
#include <sys/stat.h>
#include "common.h"

int main() {
    // Open message queue for writing, create if not exists
    mqd_t mq = mq_open(QUEUE_NAME, O_CREAT | O_WRONLY, 0644, NULL);
    if (mq == (mqd_t)-1) {
        perror("mq_open failed");
        exit(1);
    }

    const char *message = "Hello from sender! This is message queue IPC.";

    if (mq_send(mq, message, strlen(message) + 1, 0) == -1) {
        perror("mq_send failed");
        exit(1);
    }

    printf("Sender: message sent to queue '%s'\n", QUEUE_NAME);

    mq_close(mq);
    return 0;
}
