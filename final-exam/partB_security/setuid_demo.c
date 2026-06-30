#include <stdio.h>
#include <unistd.h>

int main(void) {
    uid_t real_uid = getuid();
    uid_t eff_uid = geteuid();

    printf("Real UID:      %d\n", real_uid);
    printf("Effective UID: %d\n", eff_uid);

    if (real_uid == eff_uid) {
        printf("Real and effective UID are the SAME (no privilege change).\n");
    } else {
        printf("Real and effective UID DIFFER (running with elevated/different privilege).\n");
    }

    return 0;
}
