#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <mqueue.h>
#include "common.h"

int main() {
    // Open message queue for reading
    mqd_t mq = mq_open(QUEUE_NAME, O_RDONLY);
    if (mq == (mqd_t)-1) {
        perror("mq_open failed");
        exit(1);
    }

    struct mq_attr attr;
    mq_getattr(mq, &attr);

    char buffer[MAX_SIZE + 1];
    memset(buffer, 0, sizeof(buffer));  // Clear buffer

    ssize_t bytes_read = mq_receive(mq, buffer, attr.mq_msgsize, NULL);
    if (bytes_read >= 0) {
        buffer[bytes_read] = '\0';  // Null-terminate
        printf("Receiver: message = \"%s\"\n", buffer);
    } else {
        perror("mq_receive failed");
    }

    mq_close(mq);
    mq_unlink(QUEUE_NAME); // Remove queue
    return 0;
}
