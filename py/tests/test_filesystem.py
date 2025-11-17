"""
File System Tests
"""

import unittest
from src.fs.vfs import VirtualFileSystem

class TestVirtualFileSystem(unittest.TestCase):
    def setUp(self):
        self.vfs = VirtualFileSystem()
        self.vfs.initialize()
        
    def test_create_read_file(self):
        # Test file creation
        inode = self.vfs.create_file("/test.txt", "Hello, World!")
        self.assertIsNotNone(inode)
        self.assertTrue(self.vfs.exists("/test.txt"))
        
        # Test file reading
        content = self.vfs.read_file("/test.txt")
        self.assertEqual(content, "Hello, World!")
        
    def test_directory_listing(self):
        # Test root directory listing
        contents = self.vfs.list_directory("/")
        self.assertGreater(len(contents), 0)
        
        # Check that expected directories exist
        dir_names = [f.path for f in contents]
        self.assertIn("/bin", dir_names)
        self.assertIn("/etc", dir_names)
        
    def test_file_operations(self):
        # Test file writing
        self.vfs.create_file("/test_write.txt", "Initial")
        self.vfs.write_file("/test_write.txt", "Modified")
        
        content = self.vfs.read_file("/test_write.txt")
        self.assertEqual(content, "Modified")
        
        # Test file deletion
        result = self.vfs.delete_file("/test_write.txt")
        self.assertTrue(result)
        self.assertFalse(self.vfs.exists("/test_write.txt"))
        
    def test_file_info(self):
        self.vfs.create_file("/test_info.txt", "Test content")
        
        file_info = self.vfs.get_file_info("/test_info.txt")
        self.assertIsNotNone(file_info)
        self.assertEqual(file_info.path, "/test_info.txt")
        self.assertEqual(file_info.size, len("Test content"))

if __name__ == '__main__':
    unittest.main()