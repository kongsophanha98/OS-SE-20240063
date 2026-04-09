/* winprocess.c — Process Creation on Windows using CreateProcess() */
#include <stdio.h>
#include <windows.h>

int main() {
    STARTUPINFO si;
    PROCESS_INFORMATION pi;

    ZeroMemory(&si, sizeof(si));
    si.cb = sizeof(si);
    ZeroMemory(&pi, sizeof(pi));

    printf("Parent process (PID: %lu) - launching Paint as child...\n", GetCurrentProcessId());

    const char* paintPath = "C:\\Program Files\\WindowsApps\\Microsoft.Paint_11.2601.401.0_x64__8wekyb3d8bbwe\\PaintApp\\mspaint.exe";

    if (!CreateProcess(
            paintPath,
            NULL,
            NULL, NULL, FALSE, 0, NULL, NULL,
            &si, &pi))
    {
        fprintf(stderr, "CreateProcess failed (error %lu)\n", GetLastError());
        return 1;
    }

    printf("Child process created successfully!\n");
    printf("  Child PID:       %lu\n", pi.dwProcessId);
    printf("  Child Thread ID: %lu\n", pi.dwThreadId);
    printf("\n>>> Open Task Manager NOW and take 2 screenshots!\n");
    printf("    1. Processes tab - tree view\n");
    printf("    2. Details tab - PID and Parent PID columns\n");
    printf(">>> Then close Paint to finish...\n");

    WaitForSingleObject(pi.hProcess, INFINITE);

    printf("\nParent: Paint closed. Cleaning up.\n");

    CloseHandle(pi.hProcess);
    CloseHandle(pi.hThread);

    return 0;
}