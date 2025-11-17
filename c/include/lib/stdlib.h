#ifndef STDLIB_H
#define STDLIB_H

#include "types.h"

// Function declarations
int rand(void);
void srand(unsigned int seed);
void* malloc(size_t size);
void free(void* ptr);
void* calloc(size_t num, size_t size);
void* realloc(void* ptr, size_t new_size);
int abs(int x);
long labs(long x);
int atexit(void (*func)(void));
void exit(int status);

#endif