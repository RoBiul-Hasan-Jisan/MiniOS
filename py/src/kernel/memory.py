"""
Memory Management System
"""

from include.kernel.types import *

class MemoryManager:
    def __init__(self):
        self.memory = {}
        self.next_address = 0x1000
        self.allocations = 0
        self.total_allocated = 0
        
    def initialize(self):
        """Initialize memory manager"""
        print("[MEMORY] Initializing virtual memory manager...")
        self.memory = {}
        self.allocations = 0
        self.total_allocated = 0
        
    def allocate(self, size, process_id, description="user"):
        """Allocate memory block"""
        if size <= 0:
            return None
            
        address = self.next_address
        self.memory[address] = MemoryBlock(
            address=address,
            size=size,
            process_id=process_id,
            data=[0] * size,
            description=description
        )
        
        self.next_address += size
        self.allocations += 1
        self.total_allocated += size
        
        print(f"[MEMORY] Allocated {size} bytes at 0x{address:08X} for {description}")
        return address
        
    def deallocate(self, address):
        """Deallocate memory block"""
        if address in self.memory:
            block = self.memory[address]
            self.allocations -= 1
            self.total_allocated -= block.size
            del self.memory[address]
            print(f"[MEMORY] Deallocated 0x{address:08X}")
            return True
        return False
        
    def read(self, address, offset=0, length=1):
        """Read from memory"""
        if address in self.memory:
            block = self.memory[address]
            if offset + length <= block.size:
                return block.data[offset:offset + length]
        return None
        
    def write(self, address, data, offset=0):
        """Write to memory"""
        if address in self.memory:
            block = self.memory[address]
            if offset + len(data) <= block.size:
                for i, byte in enumerate(data):
                    block.data[offset + i] = byte
                return True
        return False
        
    def get_stats(self):
        """Get memory statistics"""
        return {
            'allocations': self.allocations,
            'total_allocated': self.total_allocated,
            'free_address': self.next_address,
            'memory_blocks': list(self.memory.keys())
        }
        
    def validate_address(self, address):
        """Validate if address is allocated"""
        return address in self.memory
        
    def get_process_memory(self, process_id):
        """Get all memory blocks for a process"""
        return [block for block in self.memory.values() 
                if block.process_id == process_id]