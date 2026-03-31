# Class Activity 1 — System Calls in Practice

* Student Name: Kong Sophanha
* Student ID: p20240063

---

## Task 1: File Creator & Reader

### File Creator

The system call version uses open(), write(), and close() to create and write to a file.

### Questions

1. What flags did you use in open()?
   O_WRONLY | O_CREAT | O_TRUNC

2. What is 0644?
   File permission: owner can read/write, others can read.

---

### File Reader

The system call version reads file content using read() and prints using write().

---

## Task 2: Directory Listing

The program lists files using readdir() and retrieves file info using stat().

---

## Task 3: strace Analysis

* Library version: 38 system calls
* Syscall version: 33 system calls

Library version uses extra calls like mmap, brk, and fstat.

---

## Task 4: OS Structure

/proc is a virtual filesystem that shows system and process information.

Linux uses a monolithic kernel.

---

## Reflection

This activity helped me understand how programs interact with the OS using system calls.
