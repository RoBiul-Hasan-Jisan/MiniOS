#ifndef VFS_H
#define VFS_H

#include "types.h"

// File types
typedef enum {
    FS_FILE,
    FS_DIRECTORY
} fs_node_type_t;

// VFS node
typedef struct vfs_node {
    char name[256];
    fs_node_type_t type;
    uint32_t size;
    uint32_t inode;
    
    // File operations
    uint32_t (*read)(struct vfs_node*, uint32_t, uint32_t, uint8_t*);
    uint32_t (*write)(struct vfs_node*, uint32_t, uint32_t, uint8_t*);
    void (*open)(struct vfs_node*);
    void (*close)(struct vfs_node*);
    
    // Directory operations
    struct vfs_node* children;
    struct vfs_node* parent;
    struct vfs_node* next;
} vfs_node_t;

// Function declarations
void vfs_init(void);
vfs_node_t* vfs_get_root(void);
int vfs_mount(const char* path, vfs_node_t* fs_root);
vfs_node_t* vfs_open(const char* path, int flags);
int vfs_read(vfs_node_t* node, uint32_t offset, uint32_t size, uint8_t* buffer);
int vfs_write(vfs_node_t* node, uint32_t offset, uint32_t size, uint8_t* buffer);
void vfs_close(vfs_node_t* node);

#endif