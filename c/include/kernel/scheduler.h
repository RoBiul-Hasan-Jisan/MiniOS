#ifndef SCHEDULER_H
#define SCHEDULER_H

#include "types.h"

// Task states
typedef enum {
    TASK_UNUSED,
    TASK_READY,
    TASK_RUNNING,
    TASK_BLOCKED,
    TASK_TERMINATED
} task_state_t;

// Task priorities
typedef enum {
    TASK_PRIORITY_LOW = 1,
    TASK_PRIORITY_NORMAL = 2,
    TASK_PRIORITY_HIGH = 3
} task_priority_t;

// Process Control Block
#define MAX_TASKS 16
#define TASK_NAME_LEN 32
#define TASK_STACK_SIZE 4096
#define TIME_SLICE_BASE 10

typedef void (*task_func_t)(void);

typedef struct pcb {
    uint32_t pid;
    char name[TASK_NAME_LEN];
    task_state_t state;
    task_priority_t priority;
    uint32_t time_slice;
    uint32_t remaining_time;
    uint32_t esp;
    uint32_t ebp;
    void* stack_bottom;
    struct pcb* next;
} pcb_t;

// Function declarations
void scheduler_init(void);
int create_task(task_func_t entry, const char* name, task_priority_t priority);
void schedule(void);
void scheduler_start(void);
int get_task_count(void);
void task_exit(int exit_code);
pcb_t* get_current_task(void);

#endif