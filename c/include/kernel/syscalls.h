#ifndef SYSCALLS_H
#define SYSCALLS_H

#include "types.h"
#include "interrupt.h"

// System call numbers
#define SYS_WRITE   0
#define SYS_READ    1
#define SYS_EXIT    2
#define SYS_FORK    3
#define SYS_GETPID  4

// System call type
typedef int (*syscall_t)(int, int, int, int, int);

// Function declarations
void syscalls_init(void);
void syscall_handler(registers_t regs);
int sys_write(int fd, const char* buf, int count, int unused1, int unused2);
int sys_read(int fd, char* buf, int count, int unused1, int unused2);
int sys_exit(int status, int unused1, int unused2, int unused3, int unused4);
int sys_fork(int unused1, int unused2, int unused3, int unused4, int unused5);
int sys_getpid(int unused1, int unused2, int unused3, int unused4, int unused5);

#endif