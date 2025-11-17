#include "lib/stdlib.h"

static unsigned long next = 1;

int rand(void) {
    next = next * 1103515245 + 12345;
    return (unsigned int)(next / 65536) % 32768;
}

void srand(unsigned int seed) {
    next = seed;
}

void* malloc(size_t size) {
    return kmalloc(size);
}

void free(void* ptr) {
    kfree(ptr);
}

void* calloc(size_t num, size_t size) {
    void* ptr = kmalloc(num * size);
    if(ptr) {
        kmemset(ptr, 0, num * size);
    }
    return ptr;
}

void* realloc(void* ptr, size_t new_size) {
    if(!ptr) return kmalloc(new_size);
    
    // Simple implementation - always allocate new block
    void* new_ptr = kmalloc(new_size);
    if(new_ptr) {
        // Copy old data (would need to know old size in real implementation)
        kmemcpy(new_ptr, ptr, new_size); // This is unsafe without old size
        kfree(ptr);
    }
    return new_ptr;
}

int abs(int x) {
    return x < 0 ? -x : x;
}

long labs(long x) {
    return x < 0 ? -x : x;
}

int atexit(void (*func)(void)) {
    // Simple implementation - not supported
    return 0;
}

void exit(int status) {
    // Would call task_exit in real implementation
    while(1) asm volatile("hlt");
}