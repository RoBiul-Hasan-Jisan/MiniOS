"""
Initial RAM Disk Simulation
"""

import time
from include.kernel.types import FileType, File  # Ensure these are imported

class InitRD:
    def __init__(self):
        self.files = {}
        self.loaded = False
        
    def load(self):
        """Load initial RAM disk"""
        print("[INITRD] Loading initial RAM disk...")
        
        # Create initial file system in RAM
        self.files = {
            '/init': File(
                inode=1,
                path='/init',
                content='#!/bin/sh\necho "Starting MiniOS..."',
                size=32,
                file_type=FileType.FILE,
                created=time.time(),
                modified=time.time()
            ),
            '/etc/init.d/rc': File(
                inode=2,
                path='/etc/init.d/rc',
                content='#!/bin/sh\necho "System initialization"',
                size=40,
                file_type=FileType.FILE,
                created=time.time(),
                modified=time.time()
            )
        }
        
        self.loaded = True
        print(f"[INITRD] Loaded {len(self.files)} files into RAM")
        
    def read_file(self, path):
        """Read file from initrd"""
        if not self.loaded:
            return None
            
        file = self.files.get(path)
        return file.content if file else None
        
    def file_exists(self, path):
        """Check if file exists in initrd"""
        return path in self.files
        
    def list_files(self):
        """List all files in initrd"""
        return list(self.files.keys())
        
    def get_file_info(self, path):
        """Get file information"""
        return self.files.get(path)