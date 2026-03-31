#include <unistd.h>
#include <dirent.h>
#include <sys/stat.h>
#include <string.h>
#include <stdio.h>  // for snprintf

int main() {
    DIR *dir = opendir(".");
    if (!dir) {
        write(2, "Error opening directory\n", 24);
        return 1;
    }

    struct dirent *entry;
    struct stat fileStat;
    char buffer[512];

    // Print header
    snprintf(buffer, sizeof(buffer), "%-30s %10s\n", "Filename", "Size (bytes)");
    write(1, buffer, strlen(buffer));
    snprintf(buffer, sizeof(buffer), "%-30s %10s\n", "------------------------------", "----------");
    write(1, buffer, strlen(buffer));

    while ((entry = readdir(dir)) != NULL) {
        if (stat(entry->d_name, &fileStat) == 0) {
            snprintf(buffer, sizeof(buffer), "%-30s %10ld\n", entry->d_name, fileStat.st_size);
            write(1, buffer, strlen(buffer));
        }
    }

    closedir(dir);
    return 0;
}
