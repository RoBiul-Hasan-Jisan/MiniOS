#include "kernel/syscalls.h"
#include "kernel/scheduler.h"
#include "kernel/terminal.h"
#include "lib/string.h"

extern terminal_t main_terminal;

#define MAX_SYSCALLS 32

static syscall_t syscall_table[MAX_SYSCALLS];

void syscalls_init(void) {
    // Initialize syscall table
    kmemset(syscall_table, 0, sizeof(syscall_table));
    
    // Register system calls
    syscall_table[SYS_WRITE] = (syscall_t)sys_write;
    syscall_table[SYS_READ] = (syscall_t)sys_read;
    syscall_table[SYS_EXIT] = (syscall_t)sys_exit;
    syscall_table[SYS_FORK] = (syscall_t)sys_fork;
    syscall_table[SYS_GETPID] = (syscall_t)sys_getpid;
}

void syscall_handler(registers_t regs) {
    if(regs.eax >= MAX_SYSCALLS) return;
    
    if(syscall_table[regs.eax]) {
        syscall_t syscall = syscall_table[regs.eax];
        
        // Call system call with parameters
        int ret = syscall(regs.ebx, regs.ecx, regs.edx, regs.esi, regs.edi);
        
        // Return value in EAX
        asm volatile("mov %0, %%eax" : : "r"(ret));
    }
}

int sys_write(int fd, const char* buf, int count, int unused1, int unused2) {
    if(fd == 1) { // stdout
        for(int i = 0; i < count && buf[i] != '\0'; i++) {
            terminal_putchar(&main_terminal, buf[i]);
        }
        return count;
    }
    return -1;
}

int sys_read(int fd, char* buf, int count, int unused1, int unused2) {
    // Simple implementation - would use keyboard driver
    if(fd == 0) { // stdin
        // For now, just return empty
        buf[0] = '\0';
        return 0;
    }
    return -1;
}

int sys_exit(int status, int unused1, int unused2, int unused3, int unused4) {
    task_exit(status);
    return 0;
}

int sys_fork(int unused1, int unused2, int unused3, int unused4, int unused5) {
    // Simple fork implementation
    pcb_t* current = get_current_task();
    if(current) {
        return create_task((task_func_t)current->esp, current->name, current->priority);
    }
    return -1;
}

int sys_getpid(int unused1, int unused2, int unused3, int unused4, int unused5) {
    pcb_t* current = get_current_task();
    return current ? current->pid : -1;
}