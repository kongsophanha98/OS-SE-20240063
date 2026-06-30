#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <unistd.h>

#define NUM_THREADS 4

void *worker(void *arg) {
    long id = (long)arg;
    long computed = id * id * 10;  /* simple per-thread computation */

    printf("[Thread %ld] tid(pthread)=%lu computed value = %ld\n",
           id, (unsigned long)pthread_self(), computed);

    sleep(8);

    long *result = malloc(sizeof(long));
    *result = computed;
    pthread_exit((void *)result);
}

int main(void) {
    pthread_t threads[NUM_THREADS];
    long sum = 0;

    printf("Main: spawning %d worker threads (PID=%d)\n", NUM_THREADS, getpid());

    for (long i = 0; i < NUM_THREADS; i++) {
        if (pthread_create(&threads[i], NULL, worker, (void *)i) != 0) {
            perror("pthread_create failed");
            exit(1);
        }
    }

    for (int i = 0; i < NUM_THREADS; i++) {
        void *ret;
        if (pthread_join(threads[i], &ret) != 0) {
            perror("pthread_join failed");
            exit(1);
        }
        long *res = (long *)ret;
        printf("Main: joined thread %d, got result = %ld\n", i, *res);
        sum += *res;
        free(res);
    }

    printf("=== Summary: all %d threads joined, total = %ld ===\n", NUM_THREADS, sum);
    return 0;
}
