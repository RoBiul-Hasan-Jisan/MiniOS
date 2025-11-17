#ifndef MEMORY_H
#define MEMORY_H

#include "types.h"

// Memory manager structure
typedef struct {
    uint32_t memory_start;
    uint32_t total_memory;
    uint32_t used_memory;
    uint32_t free_memory;
} memory_manager_t;

// Function declarations
void memory_init(memory_manager_t* manager);
void* kmalloc(size_t size);
void kfree(void* ptr);
void* kmemset(void* ptr, int value, size_t num);
void* kmemcpy(void* dest, const void* src, size_t num);
void* kmemmove(void* dest, const void* src, size_t num);
int kmemcmp(const void* ptr1, const void* ptr2, size_t num);

#endif