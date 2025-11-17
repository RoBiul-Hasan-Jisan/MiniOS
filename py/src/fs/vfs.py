"""
Virtual File System
"""

import time
from include.kernel.types import FileType, File  # Ensure these are imported

class VirtualFileSystem:
    def __init__(self):
        self.files = {}
        self.mount_points = {}
        self.next_inode = 1
        
    def initialize(self):
        """Initialize VFS"""
        print("[VFS] Initializing Virtual File System...")
        self.files = {}
        
        # Create initial file system structure
        self._create_initial_filesystem()
        
    def _create_initial_filesystem(self):
        """Create initial file system structure"""
        # Create root directory
        self.create_file("/", "", FileType.DIRECTORY)
        
        # Create system directories
        directories = ["/bin", "/etc", "/home", "/tmp", "/var", "/proc", "/dev"]
        for directory in directories:
            self.create_file(directory, "", FileType.DIRECTORY)
            
        # Create system files
        system_files = [
            ("/etc/passwd", "root:x:0:0:root:/root:/bin/sh\nuser:x:1000:1000:user:/home/user:/bin/sh"),
            ("/etc/motd", "Welcome to MiniOS Python Simulation!\nThis is a simulated operating system."),
            ("/README.md", "# MiniOS Python Simulation\n\nThis is a simulated operating system written in Python."),
            ("/proc/version", "MiniOS 1.0.0 (Python Simulation)"),
            ("/proc/meminfo", "MemTotal:       16384 kB\nMemFree:         8192 kB"),
            ("/proc/cpuinfo", "processor: 0\nmodel: Python CPU Simulator\nfrequency: 1000 MHz")
        ]
        
        for path, content in system_files:
            self.create_file(path, content, FileType.FILE)
            
        # Create device files
        self.create_file("/dev/null", "", FileType.DEVICE)
        self.create_file("/dev/zero", "", FileType.DEVICE)
        self.create_file("/dev/tty", "", FileType.DEVICE)
        
    def create_file(self, path, content, file_type=FileType.FILE):
        """Create a new file"""
        inode = self.next_inode
        self.next_inode += 1
        
        file = File(
            inode=inode,
            path=path,
            content=content,
            size=len(content),
            file_type=file_type,
            created=time.time(),
            modified=time.time(),
            accessed=time.time()
        )
        
        self.files[path] = file
        print(f"[VFS] Created {file_type.name.lower()} '{path}' (inode {inode})")
        return inode
        
    def read_file(self, path):
        """Read file content"""
        if path in self.files:
            file = self.files[path]
            file.accessed = time.time()
            return file.content
        return None
        
    def write_file(self, path, content):
        """Write to file"""
        if path in self.files:
            file = self.files[path]
            file.content = content
            file.size = len(content)
            file.modified = time.time()
            return True
        return False
        
    def delete_file(self, path):
        """Delete file"""
        if path in self.files:
            del self.files[path]
            print(f"[VFS] Deleted '{path}'")
            return True
        return False
        
    def list_directory(self, path="/"):
        """List directory contents"""
        if path not in self.files or self.files[path].file_type != FileType.DIRECTORY:
            return []
            
        contents = []
        for file_path, file in self.files.items():
            if file_path.startswith(path) and file_path != path:
                # Extract the immediate child
                relative_path = file_path[len(path):].lstrip('/')
                if '/' not in relative_path or file_path.count('/') == path.count('/') + 1:
                    contents.append(file)
                    
        return contents
        
    def get_file_info(self, path):
        """Get file information"""
        return self.files.get(path)
        
    def exists(self, path):
        """Check if file exists"""
        return path in self.files
        
    def is_directory(self, path):
        """Check if path is a directory"""
        return path in self.files and self.files[path].file_type == FileType.DIRECTORY
        
    def is_file(self, path):
        """Check if path is a regular file"""
        return path in self.files and self.files[path].file_type == FileType.FILE
        
    def get_stats(self):
        """Get file system statistics"""
        total_size = sum(file.size for file in self.files.values())
        return {
            'total_files': len(self.files),
            'total_size': total_size,
            'directories': len([f for f in self.files.values() if f.file_type == FileType.DIRECTORY]),
            'regular_files': len([f for f in self.files.values() if f.file_type == FileType.FILE]),
            'devices': len([f for f in self.files.values() if f.file_type == FileType.DEVICE])
        }