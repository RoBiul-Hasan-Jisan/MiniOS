"""
System Call Handler
"""

import time
from include.kernel.constants import *

class SystemCalls:
    def __init__(self, kernel):
        self.kernel = kernel
        self.syscall_table = {}
        self._initialize_syscall_table()
        
    def _initialize_syscall_table(self):
        """Initialize system call table"""
        self.syscall_table = {
            SYS_EXIT: self.sys_exit,
            SYS_READ: self.sys_read,
            SYS_WRITE: self.sys_write,
            SYS_OPEN: self.sys_open,
            SYS_CLOSE: self.sys_close,
            SYS_BRK: self.sys_brk
        }
        
    def handle_syscall(self, syscall_number, *args):
        """Handle system call"""
        handler = self.syscall_table.get(syscall_number)
        if handler:
            return handler(*args)
        else:
            print(f"[SYSCALL] Unknown system call: {syscall_number}")
            return -1
            
    def sys_exit(self, status=0):
        """Exit current process"""
        print(f"[SYSCALL] Process exit with status {status}")
        # In a real OS, this would terminate the current process
        return 0
        
    def sys_read(self, fd, buffer, count):
        """Read from file descriptor"""
        print(f"[SYSCALL] Read {count} bytes from fd {fd}")
        # Simulate read operation
        return count
        
    def sys_write(self, fd, buffer, count):
        """Write to file descriptor"""
        print(f"[SYSCALL] Write {count} bytes to fd {fd}")
        # Simulate write operation
        return count
        
    def sys_open(self, filename, flags, mode):
        """Open a file"""
        print(f"[SYSCALL] Open file '{filename}' with flags {flags}")
        # Simulate file open - return fake file descriptor
        return 3  # Starting after stdin, stdout, stderr
        
    def sys_close(self, fd):
        """Close a file descriptor"""
        print(f"[SYSCALL] Close fd {fd}")
        return 0
        
    def sys_brk(self, addr):
        """Change data segment size"""
        print(f"[SYSCALL] brk called with address 0x{addr:x}")
        # In a real OS, this would adjust the program break
        return addr