#ifndef INITRD_H
#define INITRD_H

#include "types.h"
#include "vfs.h"

// Initrd structures
typedef struct {
    uint32_t num_files;
} initrd_header_t;

typedef struct {
    uint8_t magic;
    char name[64];
    uint32_t offset;
    uint32_t length;
} initrd_file_header_t;

// Function declarations
vfs_node_t* initrd_init(uint32_t location);

#endif