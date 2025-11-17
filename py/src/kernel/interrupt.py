"""
Interrupt Handler
"""

import queue
import threading
import time
import random
from include.kernel.constants import *

class InterruptHandler:
    def __init__(self):
        self.interrupt_queue = queue.Queue()
        self.interrupt_vectors = {}
        self.interrupt_count = 0
        self.running = True
        
    def initialize(self):
        """Initialize interrupt handler"""
        print("[INTERRUPT] Setting up interrupt descriptor table...")
        
        # Register default interrupt handlers
        self._register_default_handlers()
        
        # Start interrupt simulation thread
        sim_thread = threading.Thread(target=self._simulate_hardware_interrupts, daemon=True)
        sim_thread.start()
        
    def _register_default_handlers(self):
        """Register default interrupt handlers"""
        self.interrupt_vectors = {
            0x00: self._handle_divide_error,
            0x08: self._handle_double_fault,
            0x0D: self._handle_general_protection,
            0x20: self._handle_timer_interrupt,
            0x21: self._handle_keyboard_interrupt,
            0x80: self._handle_system_call
        }
        
    def _simulate_hardware_interrupts(self):
        """Simulate hardware interrupts"""
        interrupt_types = [
            (0x20, "TIMER", 1, 3),      # Timer interrupt
            (0x21, "KEYBOARD", 2, 5),   # Keyboard interrupt
            (0x80, "SYSCALL", 0.5, 2)   # System call
        ]
        
        while self.running:
            for vector, name, min_delay, max_delay in interrupt_types:
                if random.random() < 0.3:  # 30% chance each check
                    time.sleep(random.uniform(min_delay, max_delay))
                    self._raise_interrupt(vector, name)
                    
    def _raise_interrupt(self, vector, description):
        """Raise a simulated interrupt"""
        self.interrupt_queue.put({
            'vector': vector,
            'description': description,
            'timestamp': time.time()
        })
        self.interrupt_count += 1
        
    def process_pending(self):
        """Process pending interrupts"""
        processed = 0
        while not self.interrupt_queue.empty():
            interrupt = self.interrupt_queue.get()
            self._handle_interrupt(interrupt)
            processed += 1
            
        return processed
        
    def _handle_interrupt(self, interrupt):
        """Handle a specific interrupt"""
        vector = interrupt['vector']
        handler = self.interrupt_vectors.get(vector, self._handle_unknown_interrupt)
        handler(interrupt)
        
    def _handle_divide_error(self, interrupt):
        print(f"[INTERRUPT] Divide error at vector 0x{interrupt['vector']:02X}")
        
    def _handle_double_fault(self, interrupt):
        print(f"[INTERRUPT] Double fault at vector 0x{interrupt['vector']:02X}")
        
    def _handle_general_protection(self, interrupt):
        print(f"[INTERRUPT] General protection fault at vector 0x{interrupt['vector']:02X}")
        
    def _handle_timer_interrupt(self, interrupt):
        print(f"[INTERRUPT] Timer tick - scheduling context switch")
        
    def _handle_keyboard_interrupt(self, interrupt):
        print(f"[INTERRUPT] Keyboard input received")
        
    def _handle_system_call(self, interrupt):
        print(f"[INTERRUPT] System call invoked")
        
    def _handle_unknown_interrupt(self, interrupt):
        print(f"[INTERRUPT] Unknown interrupt 0x{interrupt['vector']:02X}")
        
    def register_handler(self, vector, handler):
        """Register a custom interrupt handler"""
        self.interrupt_vectors[vector] = handler
        
    def get_stats(self):
        """Get interrupt statistics"""
        return {
            'pending': self.interrupt_queue.qsize(),
            'total_handled': self.interrupt_count
        }