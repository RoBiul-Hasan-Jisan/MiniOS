"""
Kernel Core
"""

import time
import threading
from enum import Enum
from include.kernel.types import *
from .memory import MemoryManager
from .scheduler import Scheduler
from .terminal import Terminal
from .interrupt import InterruptHandler
from src.fs.vfs import VirtualFileSystem

class KernelState(Enum):
    BOOTING = 1
    RUNNING = 2
    SHUTDOWN = 3
    PANIC = 4

class Kernel:
    def __init__(self):
        self.state = KernelState.BOOTING
        self.version = "1.0.0"
        self.start_time = time.time()
        
        # Core subsystems
        self.memory_manager = None
        self.scheduler = None
        self.terminal = None
        self.file_system = None
        self.interrupt_handler = None
        
    def run(self):
        """Main kernel execution loop"""
        print(f"\n[KERNEL] MiniOS Kernel v{self.version} Starting...")
        
        try:
            self._initialize_subsystems()
            self.state = KernelState.RUNNING
            self._print_banner()
            
            # Main kernel loop
            self._main_loop()
            
        except Exception as e:
            self._panic(f"Kernel exception: {e}")
            
    def _initialize_subsystems(self):
        """Initialize all kernel subsystems"""
        print("[KERNEL] Initializing subsystems...")
        
        # Order matters for dependencies
        self.memory_manager = MemoryManager()
        self.memory_manager.initialize()
        
        self.interrupt_handler = InterruptHandler()
        self.interrupt_handler.initialize()
        
        self.file_system = VirtualFileSystem()
        self.file_system.initialize()
        
        self.terminal = Terminal()
        self.terminal.initialize()
        
        # Pass kernel reference to scheduler
        self.scheduler = Scheduler(kernel=self)
        self.scheduler.initialize()
        
        print("[KERNEL] All subsystems initialized")
        
    def _main_loop(self):
        """Main kernel execution loop"""
        print("[KERNEL] Entering main loop...")
        
        # Start background services
        self._start_services()
        
        # Run until shutdown
        while self.state == KernelState.RUNNING:
            # Handle interrupts
            self.interrupt_handler.process_pending()
            
            # Schedule processes
            self.scheduler.tick()
            
            # System maintenance
            self._maintenance()
            
            time.sleep(0.1)  # Simulate time slice
            
    def _start_services(self):
        """Start kernel services and initial processes"""
        print("[KERNEL] Starting services...")
        
        # Start initial user processes
        from src.apps.shell import Shell
        shell = Shell(self)
        self.scheduler.create_process("shell", shell.run, priority=2)
        
        # Start system tasks
        self.scheduler.create_process("idle_task", self._idle_task, priority=0)
        self.scheduler.create_process("logger", self._logger_task, priority=1)
        
    def _maintenance(self):
        """System maintenance tasks"""
        # Simulate occasional maintenance
        current_time = time.time()
        if int(current_time) % 10 == 0:  # Every 10 seconds
            self._cleanup_resources()
            
    def _cleanup_resources(self):
        """Clean up system resources"""
        # Simulate garbage collection
        terminated = [p for p in self.scheduler.processes.values() 
                     if p.state == ProcessState.TERMINATED]
        for process in terminated:
            if process.memory_address:
                self.memory_manager.deallocate(process.memory_address)
            if process.pid in self.scheduler.processes:
                del self.scheduler.processes[process.pid]
            
    def _idle_task(self):
        """System idle task"""
        while self.state == KernelState.RUNNING:
            time.sleep(1)
            
    def _logger_task(self):
        """System logging task"""
        while self.state == KernelState.RUNNING:
            time.sleep(5)
            print(f"[LOGGER] System uptime: {time.time() - self.start_time:.1f}s")
            
    def _print_banner(self):
        """Print system banner"""
        memory_count = len(self.memory_manager.memory) if self.memory_manager else 0
        process_count = len(self.scheduler.processes) if self.scheduler else 0
        file_count = len(self.file_system.files) if self.file_system else 0
        
        banner = f"""
┌──────────────────────────────────────┐
│             MiniOS v{self.version}            │
│      Python OS Simulation            │
│                                      │
│ Memory: {memory_count:3d} allocations    │
│ Processes: {process_count:2d} active        │
│ Files: {file_count:3d} in VFS          │
└──────────────────────────────────────┘
"""
        print(banner)
        
    def _panic(self, message):
        """Handle kernel panic"""
        self.state = KernelState.PANIC
        print(f"\n*** KERNEL PANIC ***")
        print(f"*** {message} ***")
        print("System halted.")
        
    def shutdown(self):
        """Graceful system shutdown"""
        print("\n[KERNEL] Shutting down...")
        self.state = KernelState.SHUTDOWN
        
        # Cleanup processes
        if self.scheduler:
            for process in list(self.scheduler.processes.values()):
                process.state = ProcessState.TERMINATED
            
        print("[KERNEL] Goodbye!")