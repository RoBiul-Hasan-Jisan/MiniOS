"""
Serial Port Driver Simulation
"""

import random
import time

class SerialDriver:
    def __init__(self, port=0x3F8, baud_rate=9600):
        self.port = port
        self.baud_rate = baud_rate
        self.initialized = False
        self.receive_buffer = []
        self.transmit_buffer = []
        
    def initialize(self):
        """Initialize serial port"""
        print(f"[SERIAL] Initializing COM1 (port 0x{self.port:X}) at {self.baud_rate} baud")
        
        # Set up port configuration (simulated)
        self.initialized = True
        
        # Start simulated data reception
        self._start_reception_simulation()
        
    def _start_reception_simulation(self):
        """Simulate incoming serial data"""
        def reception_loop():
            messages = [
                "SYSTEM: Ready",
                "DEBUG: Test message",
                "ERROR: Simulation error",
                "INFO: System normal"
            ]
            
            while self.initialized:
                time.sleep(random.uniform(2, 8))
                if random.random() < 0.3:  # 30% chance of message
                    message = random.choice(messages)
                    self.receive_buffer.extend(list(message + '\n'))
                    
        import threading
        thread = threading.Thread(target=reception_loop, daemon=True)
        thread.start()
        
    def send_byte(self, byte):
        """Send a byte"""
        if not self.initialized:
            return False
            
        self.transmit_buffer.append(byte)
        print(f"[SERIAL] Sent byte: 0x{byte:02X} ('{chr(byte) if 32 <= byte < 127 else '.'}')")
        return True
        
    def send_string(self, string):
        """Send a string"""
        for char in string:
            self.send_byte(ord(char))
            
    def receive_byte(self):
        """Receive a byte"""
        if self.receive_buffer:
            return ord(self.receive_buffer.pop(0))
        return None
        
    def has_data(self):
        """Check if data is available"""
        return len(self.receive_buffer) > 0
        
    def set_baud_rate(self, baud_rate):
        """Set baud rate"""
        self.baud_rate = baud_rate
        print(f"[SERIAL] Baud rate set to {baud_rate}")
        
    def get_status(self):
        """Get serial port status"""
        return {
            'port': self.port,
            'baud_rate': self.baud_rate,
            'initialized': self.initialized,
            'receive_buffer_size': len(self.receive_buffer),
            'transmit_buffer_size': len(self.transmit_buffer)
        }