#include "apps/shell.h"
#include "kernel/scheduler.h"
#include "lib/stdio.h"

void test_task1(void) {
    int counter = 0;
    while(1) {
        kprintf("Task1: Counter = %d\n", counter++);
        
        // Simple delay
        for(int i = 0; i < 1000000; i++);
        
        // Yield to other tasks
        schedule();
    }
}

void test_task2(void) {
    int counter = 100;
    while(1) {
        kprintf("Task2: Countdown = %d\n", counter--);
        
        if(counter < 0) counter = 100;
        
        // Simple delay
        for(int i = 0; i < 1000000; i++);
        
        // Yield to other tasks
        schedule();
    }
}

void test_task3(void) {
    char* message = "Hello from Task3!";
    int pos = 0;
    
    while(1) {
        kprintf("Task3: ");
        for(int i = 0; i <= pos; i++) {
            kprintf("%c", message[i]);
        }
        kprintf("\n");
        
        pos++;
        if(pos >= (int)strlen(message)) pos = 0;
        
        // Simple delay
        for(int i = 0; i < 1500000; i++);
        
        // Yield to other tasks
        schedule();
    }
}

void create_test_tasks(void) {
    kprintf("Creating test tasks...\n");
    
    create_task((task_func_t)test_task1, "test1", TASK_PRIORITY_NORMAL);
    create_task((task_func_t)test_task2, "test2", TASK_PRIORITY_NORMAL);
    create_task((task_func_t)test_task3, "test3", TASK_PRIORITY_LOW);
    
    kprintf("Test tasks created successfully\n");
}