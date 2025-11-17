"""
Process Scheduler
"""

import time
import queue
import threading
from enum import Enum
from include.kernel.types import *

class Scheduler:
    def __init__(self, kernel=None):
        self.ready_queue = queue.Queue()
        self.processes = {}
        self.current_pid = 0
        self.running_process = None
        self.ticks = 0
        self.threads = {}
        self.kernel = kernel  # Store kernel reference
        
    def initialize(self):
        """Initialize scheduler"""
        print("[SCHEDULER] Initializing process scheduler...")
        self.processes = {}
        self.current_pid = 0
        
        # Create initial system processes
        self.create_process("kernel_main", self._kernel_main_task, priority=0)
        
    def create_process(self, name, entry_point, priority=1, memory_size=1024):
        """Create new process"""
        pid = self._generate_pid()
        
        # Allocate process memory
        memory_address = None
        if self.kernel and self.kernel.memory_manager:
            memory_address = self.kernel.memory_manager.allocate(memory_size, pid, f"process_{name}")
        
        process = Process(
            pid=pid,
            name=name,
            entry_point=entry_point,
            priority=priority,
            memory_address=memory_address,
            created_time=time.time()
        )
        
        self.processes[pid] = process
        self.ready_queue.put(process)
        
        # Start process in background thread
        thread = threading.Thread(target=self._run_process, args=(process,), daemon=True)
        self.threads[pid] = thread
        thread.start()
        
        print(f"[SCHEDULER] Created process {pid}: {name} (priority {priority})")
        return pid
        
    def _generate_pid(self):
        """Generate unique process ID"""
        self.current_pid += 1
        return self.current_pid
        
    def _run_process(self, process):
        """Run a process in its own thread"""
        try:
            process.state = ProcessState.RUNNING
            if callable(process.entry_point):
                process.entry_point()
            else:
                print(f"[SCHEDULER] Process {process.pid} has non-callable entry point")
                
        except Exception as e:
            print(f"[SCHEDULER] Process {process.pid} crashed: {e}")
        finally:
            process.state = ProcessState.TERMINATED
            print(f"[SCHEDULER] Process {process.pid} terminated")
        
    def tick(self):
        """Scheduler timer tick"""
        self.ticks += 1
        
        # Every 5 ticks, do scheduling decisions
        if self.ticks % 5 == 0:
            self._schedule()
            
    def _schedule(self):
        """Make scheduling decisions"""
        # Simple round-robin simulation
        active_processes = [p for p in self.processes.values() 
                          if p.state != ProcessState.TERMINATED]
        
        if active_processes:
            # Simulate context switching
            if self.running_process:
                self.running_process.state = ProcessState.READY
                
            # Get next process (simple round-robin)
            next_process = None
            for pid, process in self.processes.items():
                if process.state == ProcessState.READY:
                    next_process = process
                    break
                    
            if next_process:
                self.running_process = next_process
                self.running_process.state = ProcessState.RUNNING
                print(f"[SCHEDULER] Context switch to PID {next_process.pid}")
                
    def terminate_process(self, pid):
        """Terminate a process"""
        if pid in self.processes:
            process = self.processes[pid]
            process.state = ProcessState.TERMINATED
            
            # Clean up memory if kernel is available
            if self.kernel and self.kernel.memory_manager and process.memory_address:
                self.kernel.memory_manager.deallocate(process.memory_address)
            
            # Clean up thread
            if pid in self.threads:
                del self.threads[pid]
                
            print(f"[SCHEDULER] Terminated process {pid}")
            return True
        return False
            
    def list_processes(self):
        """List all processes"""
        return list(self.processes.values())
        
    def get_process_info(self, pid):
        """Get information about a specific process"""
        return self.processes.get(pid)
        
    def _kernel_main_task(self):
        """Kernel main task"""
        while True:
            time.sleep(10)
            print(f"[KERNEL_TASK] System tick - {self.ticks} scheduler ticks")