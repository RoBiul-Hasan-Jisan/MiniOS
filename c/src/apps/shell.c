#include "apps/shell.h"
#include "kernel/terminal.h"
#include "lib/string.h"
#include "lib/stdio.h"
#include "drivers/keyboard.h"

extern terminal_t main_terminal;

#define MAX_INPUT_LEN 256
#define MAX_ARGS 16

static char input_buffer[MAX_INPUT_LEN];
static int input_pos = 0;

// Command structure
typedef struct {
    const char* name;
    const char* description;
    void (*function)(int argc, char** argv);
} command_t;

// Command implementations
void cmd_help(int argc, char** argv) {
    kprintf("Available commands:\n");
    kprintf("help     - Show this help message\n");
    kprintf("clear    - Clear the screen\n");
    kprintf("echo     - Echo arguments\n");
    kprintf("meminfo  - Show memory information\n");
    kprintf("tasks    - List running tasks\n");
    kprintf("calc     - Simple calculator\n");
    kprintf("reboot   - Reboot system\n");
    kprintf("shutdown - Shutdown system\n");
    kprintf("exit     - Exit shell\n");
}

void cmd_clear(int argc, char** argv) {
    terminal_clear(&main_terminal);
}

void cmd_echo(int argc, char** argv) {
    for(int i = 1; i < argc; i++) {
        kprintf("%s ", argv[i]);
    }
    kprintf("\n");
}

void cmd_meminfo(int argc, char** argv) {
    extern memory_manager_t mem_manager;
    kprintf("Memory Information:\n");
    kprintf("Total: %d KB\n", mem_manager.total_memory / 1024);
    kprintf("Used: %d KB\n", mem_manager.used_memory / 1024);
    kprintf("Free: %d KB\n", mem_manager.free_memory / 1024);
    kprintf("Usage: %d%%\n", (mem_manager.used_memory * 100) / mem_manager.total_memory);
}

void cmd_tasks(int argc, char** argv) {
    kprintf("Task list functionality not implemented yet\n");
}

void cmd_calc(int argc, char** argv) {
    if(argc != 4) {
        kprintf("Usage: calc <num1> <op> <num2>\n");
        kprintf("Operations: +, -, *, /\n");
        return;
    }
    
    int num1 = atoi(argv[1]);
    int num2 = atoi(argv[3]);
    char op = argv[2][0];
    int result = 0;
    
    switch(op) {
        case '+': result = num1 + num2; break;
        case '-': result = num1 - num2; break;
        case '*': result = num1 * num2; break;
        case '/': 
            if(num2 != 0) result = num1 / num2;
            else { kprintf("Error: Division by zero\n"); return; }
            break;
        default: kprintf("Error: Invalid operator '%c'\n", op); return;
    }
    
    kprintf("Result: %d %c %d = %d\n", num1, op, num2, result);
}

void cmd_reboot(int argc, char** argv) {
    kprintf("Rebooting system...\n");
    // Would trigger system reboot
    asm volatile("cli");
    asm volatile("hlt");
}

void cmd_shutdown(int argc, char** argv) {
    kprintf("Shutting down system...\n");
    // Would trigger system shutdown
    asm volatile("cli");
    asm volatile("hlt");
}

// Command table
static command_t commands[] = {
    {"help", "Show help", cmd_help},
    {"clear", "Clear screen", cmd_clear},
    {"echo", "Echo arguments", cmd_echo},
    {"meminfo", "Memory information", cmd_meminfo},
    {"tasks", "List tasks", cmd_tasks},
    {"calc", "Calculator", cmd_calc},
    {"reboot", "Reboot system", cmd_reboot},
    {"shutdown", "Shutdown system", cmd_shutdown},
    {NULL, NULL, NULL}
};

void shell_main(void) {
    kprintf("MiniOS Shell v1.0\n");
    kprintf("Type 'help' for available commands\n");
    
    while(1) {
        kprintf("minios> ");
        shell_read_input();
        shell_execute_command();
    }
}

void shell_read_input(void) {
    input_pos = 0;
    input_buffer[0] = '\0';
    
    while(1) {
        char c = keyboard_getchar();
        
        if(c == '\n') {
            kprintf("\n");
            break;
        } else if(c == '\b') {
            if(input_pos > 0) {
                input_pos--;
                kprintf("\b \b");
            }
        } else if(c >= 32 && c <= 126 && input_pos < MAX_INPUT_LEN - 1) {
            input_buffer[input_pos++] = c;
            input_buffer[input_pos] = '\0';
            kprintf("%c", c);
        }
    }
}

void shell_execute_command(void) {
    if(input_pos == 0) return;
    
    char* args[MAX_ARGS];
    int argc = 0;
    
    // Tokenize input
    char* token = strtok(input_buffer, " ");
    while(token && argc < MAX_ARGS - 1) {
        args[argc++] = token;
        token = strtok(NULL, " ");
    }
    args[argc] = NULL;
    
    if(argc == 0) return;
    
    // Handle exit command specially
    if(strcmp(args[0], "exit") == 0) {
        kprintf("Logging out...\n");
        task_exit(0);
        return;
    }
    
    // Find and execute command
    for(int i = 0; commands[i].name != NULL; i++) {
        if(strcmp(args[0], commands[i].name) == 0) {
            commands[i].function(argc, args);
            return;
        }
    }
    
    kprintf("Command not found: %s\n", args[0]);
    kprintf("Type 'help' for available commands\n");
}