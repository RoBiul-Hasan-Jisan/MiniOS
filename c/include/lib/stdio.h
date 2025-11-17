#ifndef STDIO_H
#define STDIO_H

#include "types.h"

// Variable argument macros
typedef __builtin_va_list va_list;
#define va_start(v,l) __builtin_va_start(v,l)
#define va_end(v) __builtin_va_end(v)
#define va_arg(v,l) __builtin_va_arg(v,l)

// Function declarations
int atoi(const char* str);
char* itoa(int value, char* str, int base);
int vsprintf(char* str, const char* format, va_list args);
int sprintf(char* str, const char* format, ...);

#endif