#include "kernel/memory.h"
#include "lib/string.h"

#define MEMORY_POOL_SIZE (1024 * 1024) // 1MB
#define BLOCK_SIZE 32

typedef struct memory_block {
    struct memory_block* next;
    size_t size;
    int free;
} memory_block_t;

static memory_manager_t mem_manager;

void memory_init(memory_manager_t* manager) {
    manager->memory_start = 0x100000; // 1MB mark
    manager->total_memory = MEMORY_POOL_SIZE;
    manager->used_memory = 0;
    manager->free_memory = MEMORY_POOL_SIZE;
    
    // Initialize first block
    memory_block_t* first_block = (memory_block_t*)manager->memory_start;
    first_block->size = MEMORY_POOL_SIZE - sizeof(memory_block_t);
    first_block->free = 1;
    first_block->next = NULL;
}

void* kmalloc(size_t size) {
    memory_manager_t* manager = &mem_manager;
    
    if(size == 0) return NULL;
    
    // Align size
    size = (size + BLOCK_SIZE - 1) & ~(BLOCK_SIZE - 1);
    
    memory_block_t* current = (memory_block_t*)manager->memory_start;
    memory_block_t* best_fit = NULL;
    
    // Best fit algorithm
    while(current) {
        if(current->free && current->size >= size) {
            if(!best_fit || current->size < best_fit->size) {
                best_fit = current;
            }
        }
        current = current->next;
    }
    
    if(!best_fit) return NULL; // Out of memory
    
    // Split block if possible
    if(best_fit->size > size + sizeof(memory_block_t) + BLOCK_SIZE) {
        memory_block_t* new_block = (memory_block_t*)((char*)best_fit + sizeof(memory_block_t) + size);
        new_block->size = best_fit->size - size - sizeof(memory_block_t);
        new_block->free = 1;
        new_block->next = best_fit->next;
        
        best_fit->size = size;
        best_fit->next = new_block;
    }
    
    best_fit->free = 0;
    manager->used_memory += best_fit->size + sizeof(memory_block_t);
    manager->free_memory -= best_fit->size + sizeof(memory_block_t);
    
    return (void*)((char*)best_fit + sizeof(memory_block_t));
}

void kfree(void* ptr) {
    if(!ptr) return;
    
    memory_manager_t* manager = &mem_manager;
    memory_block_t* block = (memory_block_t*)((char*)ptr - sizeof(memory_block_t));
    
    block->free = 1;
    manager->used_memory -= block->size + sizeof(memory_block_t);
    manager->free_memory += block->size + sizeof(memory_block_t);
    
    // Merge with next block if free
    if(block->next && block->next->free) {
        block->size += block->next->size + sizeof(memory_block_t);
        block->next = block->next->next;
    }
}

void* kmemset(void* ptr, int value, size_t num) {
    unsigned char* p = (unsigned char*)ptr;
    while(num--) {
        *p++ = (unsigned char)value;
    }
    return ptr;
}

void* kmemcpy(void* dest, const void* src, size_t num) {
    unsigned char* d = (unsigned char*)dest;
    const unsigned char* s = (const unsigned char*)src;
    while(num--) {
        *d++ = *s++;
    }
    return dest;
}

void* kmemmove(void* dest, const void* src, size_t num) {
    unsigned char* d = (unsigned char*)dest;
    const unsigned char* s = (const unsigned char*)src;
    
    if(d < s) {
        while(num--) {
            *d++ = *s++;
        }
    } else {
        d += num;
        s += num;
        while(num--) {
            *--d = *--s;
        }
    }
    return dest;
}

int kmemcmp(const void* ptr1, const void* ptr2, size_t num) {
    const unsigned char* p1 = (const unsigned char*)ptr1;
    const unsigned char* p2 = (const unsigned char*)ptr2;
    
    while(num--) {
        if(*p1 != *p2) {
            return *p1 - *p2;
        }
        p1++;
        p2++;
    }
    return 0;
}