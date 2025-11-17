#include "kernel/scheduler.h"
#include "kernel/memory.h"
#include "lib/string.h"

static pcb_t tasks[MAX_TASKS];
static pcb_t* current_task = NULL;
static pcb_t* ready_queue = NULL;
static int next_pid = 1;
static int task_count = 0;

void scheduler_init(void) {
    kmemset(tasks, 0, sizeof(tasks));
    current_task = NULL;
    ready_queue = NULL;
    next_pid = 1;
    task_count = 0;
}

int create_task(task_func_t entry, const char* name, task_priority_t priority) {
    if(task_count >= MAX_TASKS) return -1;
    
    // Find free task slot
    int slot = -1;
    for(int i = 0; i < MAX_TASKS; i++) {
        if(tasks[i].state == TASK_TERMINATED || tasks[i].state == TASK_UNUSED) {
            slot = i;
            break;
        }
    }
    
    if(slot == -1) return -1;
    
    pcb_t* task = &tasks[slot];
    
    // Initialize task structure
    task->pid = next_pid++;
    kstrncpy(task->name, name, TASK_NAME_LEN - 1);
    task->name[TASK_NAME_LEN - 1] = '\0';
    task->state = TASK_READY;
    task->priority = priority;
    task->time_slice = priority * TIME_SLICE_BASE;
    task->remaining_time = task->time_slice;
    
    // Allocate stack
    task->stack_bottom = kmalloc(TASK_STACK_SIZE);
    if(!task->stack_bottom) return -1;
    
    // Set up initial stack
    uint32_t* stack_top = (uint32_t*)((char*)task->stack_bottom + TASK_STACK_SIZE);
    
    // Push initial context
    *(--stack_top) = (uint32_t)entry;  // EIP
    *(--stack_top) = 0x202;           // EFLAGS
    *(--stack_top) = 0x08;            // CS
    *(--stack_top) = 0x10;            // DS/ES/FS/GS/SS
    
    task->esp = (uint32_t)stack_top;
    task->ebp = task->esp;
    
    // Add to ready queue
    task->next = ready_queue;
    ready_queue = task;
    
    task_count++;
    return task->pid;
}

void schedule(void) {
    if(!ready_queue) return;
    
    // Round-robin scheduling
    pcb_t* prev = NULL;
    pcb_t* curr = ready_queue;
    
    while(curr && curr->remaining_time <= 0) {
        curr->remaining_time = curr->time_slice;
        prev = curr;
        curr = curr->next;
    }
    
    if(!curr) {
        // Reset all time slices
        curr = ready_queue;
        while(curr) {
            curr->remaining_time = curr->time_slice;
            curr = curr->next;
        }
        curr = ready_queue;
    }
    
    if(curr && curr != current_task) {
        if(current_task && current_task->state == TASK_RUNNING) {
            current_task->state = TASK_READY;
        }
        
        current_task = curr;
        current_task->state = TASK_RUNNING;
        current_task->remaining_time--;
    }
}

void scheduler_start(void) {
    if(ready_queue) {
        current_task = ready_queue;
        current_task->state = TASK_RUNNING;
    }
}

int get_task_count(void) {
    return task_count;
}

void task_exit(int exit_code) {
    if(current_task) {
        current_task->state = TASK_TERMINATED;
        kfree(current_task->stack_bottom);
        task_count--;
        schedule();
    }
}

pcb_t* get_current_task(void) {
    return current_task;
}