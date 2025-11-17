#include "fs/initrd.h"

static initrd_header_t* initrd_header = NULL;
static initrd_file_header_t* file_headers = NULL;
static vfs_node_t* initrd_root = NULL;

static uint32_t initrd_read(vfs_node_t* node, uint32_t offset, uint32_t size, uint8_t* buffer) {
    initrd_file_header_t header = file_headers[node->inode];
    
    if(offset > header.length) return 0;
    if(offset + size > header.length) size = header.length - offset;
    
    kmemcpy(buffer, (uint8_t*)(header.offset + offset), size);
    return size;
}

static void initrd_close(vfs_node_t* node) {
    // Nothing to do
}

vfs_node_t* initrd_init(uint32_t location) {
    initrd_header = (initrd_header_t*)location;
    file_headers = (initrd_file_header_t*)(location + sizeof(initrd_header_t));
    
    // Create root node
    initrd_root = kmalloc(sizeof(vfs_node_t));
    if(!initrd_root) return NULL;
    
    kstrcpy(initrd_root->name, "initrd");
    initrd_root->type = FS_DIRECTORY;
    initrd_root->read = NULL;
    initrd_root->write = NULL;
    initrd_root->open = NULL;
    initrd_root->close = NULL;
    initrd_root->children = NULL;
    initrd_root->parent = NULL;
    initrd_root->next = NULL;
    
    // Create file nodes
    for(uint32_t i = 0; i < initrd_header->num_files; i++) {
        vfs_node_t* file = kmalloc(sizeof(vfs_node_t));
        if(!file) continue;
        
        kstrcpy(file->name, file_headers[i].name);
        file->type = FS_FILE;
        file->size = file_headers[i].length;
        file->inode = i;
        file->read = initrd_read;
        file->write = NULL;
        file->open = NULL;
        file->close = initrd_close;
        file->children = NULL;
        file->parent = initrd_root;
        file->next = initrd_root->children;
        
        initrd_root->children = file;
    }
    
    return initrd_root;
}