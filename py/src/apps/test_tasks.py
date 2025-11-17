"""
Test Tasks Application
"""

import time
import random
from src.lib.stdio import Stdio

class TestTasks:
    def __init__(self, kernel):
        self.kernel = kernel
        
    def run_cpu_test(self):
        """CPU performance test"""
        Stdio.printf("Running CPU test...\n")
        start_time = time.time()
        
        # Simple CPU stress test
        result = 0
        for i in range(1000000):
            result = (result + i) % 1000
            
        end_time = time.time()
        duration = end_time - start_time
        Stdio.printf("CPU test completed in %.3f seconds\n", duration)
        return duration
        
    def run_memory_test(self):
        """Memory performance test"""
        Stdio.printf("Running memory test...\n")
        start_time = time.time()
        
        # Allocate and manipulate memory
        test_size = 10000
        test_data = [random.randint(0, 255) for _ in range(test_size)]
        
        # Perform operations
        for i in range(1000):
            test_data[i % test_size] = (test_data[i % test_size] + 1) % 256
            
        end_time = time.time()
        duration = end_time - start_time
        Stdio.printf("Memory test completed in %.3f seconds\n", duration)
        return duration
        
    def run_file_system_test(self):
        """File system performance test"""
        Stdio.printf("Running file system test...\n")
        start_time = time.time()
        
        # Create test file
        test_content = "x" * 1000
        self.kernel.file_system.create_file("/tmp/test_file", test_content)
        
        # Read it back
        content = self.kernel.file_system.read_file("/tmp/test_file")
        
        # Verify
        if content == test_content:
            Stdio.printf("File system test: PASS\n")
        else:
            Stdio.printf("File system test: FAIL\n")
            
        end_time = time.time()
        duration = end_time - start_time
        Stdio.printf("File system test completed in %.3f seconds\n", duration)
        return duration
        
    def run_all_tests(self):
        """Run all performance tests"""
        Stdio.printf("=== MiniOS Performance Tests ===\n\n")
        
        results = {}
        results['cpu'] = self.run_cpu_test()
        results['memory'] = self.run_memory_test()
        results['filesystem'] = self.run_file_system_test()
        
        Stdio.printf("\n=== Test Summary ===\n")
        for test_name, duration in results.items():
            Stdio.printf("%-12s: %.3f seconds\n", test_name.capitalize(), duration)
            
        return results