#include <stdio.h>
#include <stdlib.h>
#include <signal.h>
#include <unistd.h>

volatile sig_atomic_t keep_running = 1;
volatile sig_atomic_t last_signal = 0;

void handle_signal(int sig) {
    last_signal = sig;
    keep_running = 0;
}

int main(void) {
    struct sigaction sa;
    sa.sa_handler = handle_signal;
    sigemptyset(&sa.sa_mask);
    sa.sa_flags = 0;

    if (sigaction(SIGINT, &sa, NULL) == -1) {
        perror("sigaction SIGINT failed");
        exit(1);
    }
    if (sigaction(SIGTERM, &sa, NULL) == -1) {
        perror("sigaction SIGTERM failed");
        exit(1);
    }

    printf("signal_demo running, PID=%d. Send SIGINT (Ctrl+C) or SIGTERM to stop.\n", getpid());

    int count = 0;
    while (keep_running) {
        printf("[%d] still running...\n", count++);
        sleep(1);
    }

    printf("\nCaught signal %d (%s). Cleaning up...\n",
           last_signal, last_signal == SIGINT ? "SIGINT" : "SIGTERM");
    printf("Cleanup complete. Exiting gracefully.\n");

    return 0;
}
