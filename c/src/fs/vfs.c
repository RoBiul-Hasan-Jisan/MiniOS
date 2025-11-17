#include "fs/vfs.h"

static vfs_node_t* root_node = NULL;

void vfs_init(void) {
    root_node = kmalloc(sizeof(vfs_node_t));
    if(root_node) {
        kstrcpy(root_node->name, "/");
        root_node->type = FS_DIRECTORY;
        root_node->size = 0;
        root_node->read = NULL;
        root_node->write = NULL;
        root_node->open = NULL;
        root_node->close = NULL;
        root_node->children = NULL;
        root_node->parent = NULL;
        root_node->next = NULL;
    }
}

vfs_node_t* vfs_get_root(void) {
    return root_node;
}

int vfs_mount(const char* path, vfs_node_t* fs_root) {
    // Simple mount implementation
    if(!root_node || !fs_root) return -1;
    
    vfs_node_t* node = kmalloc(sizeof(vfs_node_t));
    if(!node) return -1;
    
    kmemcpy(node, fs_root, sizeof(vfs_node_t));
    node->next = root_node->children;
    root_node->children = node;
    
    return 0;
}

vfs_node_t* vfs_open(const char* path, int flags) {
    // Simple open implementation
    if(!root_node) return NULL;
    
    // For now, just return root for any path
    return root_node;
}

int vfs_read(vfs_node_t* node, uint32_t offset, uint32_t size, uint8_t* buffer) {
    if(!node || !node->read) return -1;
    return node->read(node, offset, size, buffer);
}

int vfs_write(vfs_node_t* node, uint32_t offset, uint32_t size, uint8_t* buffer) {
    if(!node || !node->write) return -1;
    return node->write(node, offset, size, buffer);
}

void vfs_close(vfs_node_t* node) {
    if(node && node->close) {
        node->close(node);
    }
}