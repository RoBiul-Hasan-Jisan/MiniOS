"""
Process Scheduler Tests
"""

import unittest
import time
from src.kernel.scheduler import Scheduler

def dummy_task():
    time.sleep(0.1)

class TestScheduler(unittest.TestCase):
    def setUp(self):
        self.scheduler = Scheduler()
        self.scheduler.initialize()
        
    def test_create_process(self):
        pid = self.scheduler.create_process("test_task", dummy_task)
        self.assertIsNotNone(pid)
        self.assertIn(pid, self.scheduler.processes)
        
        process = self.scheduler.processes[pid]
        self.assertEqual(process.name, "test_task")
        self.assertEqual(process.priority, 1)
        
    def test_terminate_process(self):
        pid = self.scheduler.create_process("test_task", dummy_task)
        
        # Give it a moment to start
        time.sleep(0.1)
        
        result = self.scheduler.terminate_process(pid)
        self.assertTrue(result)
        self.assertNotIn(pid, self.scheduler.threads)
        
    def test_list_processes(self):
        # Create multiple processes
        pids = []
        for i in range(3):
            pid = self.scheduler.create_process(f"task_{i}", dummy_task)
            pids.append(pid)
            
        processes = self.scheduler.list_processes()
        self.assertEqual(len(processes), 4)  # 3 + kernel_main
        
        # Check that our processes are in the list
        process_names = [p.name for p in processes]
        for i in range(3):
            self.assertIn(f"task_{i}", process_names)

if __name__ == '__main__':
    unittest.main()