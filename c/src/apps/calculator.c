#include "apps/calculator.h"
#include "lib/stdio.h"
#include "lib/string.h"

void calculator_main(void) {
    kprintf("MiniOS Calculator v1.0\n");
    kprintf("Enter expressions like: 2 + 3 * 4\n");
    kprintf("Operations: +, -, *, /, %%\n");
    kprintf("Type 'quit' to exit\n\n");
    
    char input[100];
    
    while(1) {
        kprintf("calc> ");
        
        // Simple input reading
        char c;
        int pos = 0;
        while((c = keyboard_getchar()) != '\n' && pos < 99) {
            if(c == '\b') {
                if(pos > 0) {
                    pos--;
                    kprintf("\b \b");
                }
            } else if(c >= 32 && c <= 126) {
                input[pos++] = c;
                input[pos] = '\0';
                kprintf("%c", c);
            }
        }
        kprintf("\n");
        
        if(strcmp(input, "quit") == 0) {
            break;
        }
        
        // Simple expression evaluation
        int num1, num2, result;
        char op;
        
        if(sscanf(input, "%d %c %d", &num1, &op, &num2) == 3) {
            switch(op) {
                case '+': result = num1 + num2; break;
                case '-': result = num1 - num2; break;
                case '*': result = num1 * num2; break;
                case '/': 
                    if(num2 != 0) result = num1 / num2;
                    else { kprintf("Error: Division by zero\n"); continue; }
                    break;
                case '%': 
                    if(num2 != 0) result = num1 % num2;
                    else { kprintf("Error: Modulo by zero\n"); continue; }
                    break;
                default: 
                    kprintf("Error: Unknown operator '%c'\n", op);
                    continue;
            }
            kprintf("Result: %d\n", result);
        } else {
            kprintf("Error: Invalid expression format\n");
            kprintf("Use: <number> <operator> <number>\n");
        }
    }
    
    kprintf("Calculator exited\n");
}

int sscanf(const char* str, const char* format, ...) {
    // Simple sscanf implementation for basic patterns
    va_list args;
    va_start(args, format);
    
    int count = 0;
    const char* s = str;
    
    while(*format) {
        if(*format == '%') {
            format++;
            switch(*format) {
                case 'd': {
                    int* num = va_arg(args, int*);
                    *num = 0;
                    int sign = 1;
                    
                    // Skip whitespace
                    while(*s == ' ') s++;
                    
                    // Handle sign
                    if(*s == '-') {
                        sign = -1;
                        s++;
                    } else if(*s == '+') {
                        s++;
                    }
                    
                    // Read digits
                    while(*s >= '0' && *s <= '9') {
                        *num = *num * 10 + (*s - '0');
                        s++;
                    }
                    *num *= sign;
                    count++;
                    break;
                }
                case 'c': {
                    char* ch = va_arg(args, char*);
                    // Skip whitespace
                    while(*s == ' ') s++;
                    *ch = *s++;
                    count++;
                    break;
                }
                case 's': {
                    char* str_out = va_arg(args, char*);
                    // Skip whitespace
                    while(*s == ' ') s++;
                    // Read until whitespace
                    while(*s && *s != ' ') {
                        *str_out++ = *s++;
                    }
                    *str_out = '\0';
                    count++;
                    break;
                }
            }
        } else {
            // Match literal characters
            if(*s != *format) break;
            s++;
        }
        format++;
    }
    
    va_end(args);
    return count;
}