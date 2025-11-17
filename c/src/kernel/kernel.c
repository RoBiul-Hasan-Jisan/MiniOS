#include "kernel/kernel.h"
#include "drivers/vga.h"
#include "drivers/keyboard.h"
#include "kernel/terminal.h"
#include "kernel/memory.h"
#include "kernel/scheduler.h"
#include "kernel/syscalls.h"
#include "kernel/interrupt.h"
#include "kernel/timer.h"
#include "apps/shell.h"

// Kernel version information
const char* KERNEL_VERSION = "MiniOS v1.0";
const char* KERNEL_BUILD_DATE = __DATE__ " " __TIME__;

// Global kernel structures
terminal_t main_terminal;
memory_manager_t mem_manager;

// Kernel entry point
void kernel_main(void) {
    // Initialize terminal
    terminal_initialize(&main_terminal, COLOR_WHITE, COLOR_BLACK);
    
    // Print welcome message
    terminal_writestring(&main_terminal, "Booting ");
    terminal_writestring(&main_terminal, KERNEL_VERSION);
    terminal_writestring(&main_terminal, "\nBuild: ");
    terminal_writestring(&main_terminal, KERNEL_BUILD_DATE);
    terminal_writestring(&main_terminal, "\n\n");
    
    // Initialize systems
    kprintf("Initializing memory manager... ");
    memory_init(&mem_manager);
    kprintf("OK\n");
    
    kprintf("Initializing interrupts... ");
    idt_init();
    kprintf("OK\n");
    
    kprintf("Initializing system calls... ");
    syscalls_init();
    kprintf("OK\n");
    
    kprintf("Initializing keyboard... ");
    keyboard_init();
    kprintf("OK\n");
    
    kprintf("Initializing timer... ");
    timer_init(100); // 100 Hz
    kprintf("OK\n");
    
    kprintf("Initializing scheduler... ");
    scheduler_init();
    kprintf("OK\n");
    
    // Create system tasks
    kprintf("Creating system tasks... ");
    create_task((task_func_t)shell_main, "shell", TASK_PRIORITY_NORMAL);
    create_task((task_func_t)idle_task, "idle", TASK_PRIORITY_LOW);
    kprintf("OK\n\n");
    
    // Show system information
    kprintf("Memory: %d KB available\n", mem_manager.total_memory / 1024);
    kprintf("Tasks: %d created\n", get_task_count());
    kprintf("\nMiniOS Ready!\n");
    kprintf("Type 'help' for available commands\n\n");
    
    // Start multitasking
    scheduler_start();
    
    // Should never reach here
    while(1) {
        asm volatile("hlt");
    }
}

// Kernel print function
void kprintf(const char* format, ...) {
    char buffer[256];
    va_list args;
    va_start(args, format);
    vsprintf(buffer, format, args);
    va_end(args);
    terminal_writestring(&main_terminal, buffer);
}

// Idle task
void idle_task(void) {
    while(1) {
        asm volatile("hlt");
    }
}