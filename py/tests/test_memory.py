"""
Memory Management Tests
"""

import unittest
from src.kernel.memory import MemoryManager

class TestMemoryManager(unittest.TestCase):
    def setUp(self):
        self.memory = MemoryManager()
        self.memory.initialize()
        
    def test_allocate_deallocate(self):
        # Test basic allocation
        addr = self.memory.allocate(1024, 1, "test")
        self.assertIsNotNone(addr)
        self.assertIn(addr, self.memory.memory)
        
        # Test deallocation
        result = self.memory.deallocate(addr)
        self.assertTrue(result)
        self.assertNotIn(addr, self.memory.memory)
        
    def test_read_write(self):
        addr = self.memory.allocate(100, 1, "test_rw")
        
        # Test write
        data = [1, 2, 3, 4, 5]
        result = self.memory.write(addr, data)
        self.assertTrue(result)
        
        # Test read
        read_data = self.memory.read(addr, 0, 5)
        self.assertEqual(read_data, data)
        
    def test_invalid_operations(self):
        # Test allocation with invalid size
        addr = self.memory.allocate(0, 1, "invalid")
        self.assertIsNone(addr)
        
        # Test deallocation of invalid address
        result = self.memory.deallocate(0x123456)
        self.assertFalse(result)
        
    def test_memory_stats(self):
        # Allocate some memory
        self.memory.allocate(512, 1, "test1")
        self.memory.allocate(1024, 2, "test2")
        
        stats = self.memory.get_stats()
        self.assertEqual(stats['allocations'], 2)
        self.assertEqual(stats['total_allocated'], 512 + 1024)

if __name__ == '__main__':
    unittest.main()