#include <fcntl.h>
#include <unistd.h>
#include <string.h>

int main() {
    const char *text = "Hello from Operating Systems class!\n";
    int fd = open("output.txt", O_WRONLY | O_CREAT | O_TRUNC, 0644);
    if (fd < 0) {
        write(2, "Error opening file\n", 19);
        return 1;
    }

    write(fd, text, strlen(text));
    close(fd);

    const char *confirm = "File created successfully!\n";
    write(1, confirm, strlen(confirm));

    return 0;
}
