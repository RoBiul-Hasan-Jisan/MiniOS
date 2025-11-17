"""
Keyboard Driver Simulation
"""

import threading
import time
import random

class KeyboardDriver:
    def __init__(self):
        self.key_buffer = []
        self.interrupt_enabled = True
        self.last_key = None
        self.shift_pressed = False
        self.ctrl_pressed = False
        self.alt_pressed = False
        
    def initialize(self):
        """Initialize keyboard driver"""
        print("[KEYBOARD] Initializing keyboard driver...")
        
        # Start simulated key press thread
        sim_thread = threading.Thread(target=self._simulate_key_presses, daemon=True)
        sim_thread.start()
        
    def _simulate_key_presses(self):
        """Simulate random key presses"""
        keys = "abcdefghijklmnopqrstuvwxyz0123456789 \r\x7f"
        
        while True:
            time.sleep(random.uniform(1, 5))
            if random.random() < 0.4:  # 40% chance of key press
                key = random.choice(keys)
                self._key_pressed(key)
                
    def _key_pressed(self, key):
        """Handle key press event"""
        self.key_buffer.append(key)
        self.last_key = key
        
        if self.interrupt_enabled:
            print(f"[KEYBOARD] Key pressed: {repr(key)}")
            
    def get_key(self):
        """Get next key from buffer"""
        if self.key_buffer:
            return self.key_buffer.pop(0)
        return None
        
    def has_key(self):
        """Check if key is available"""
        return len(self.key_buffer) > 0
        
    def flush_buffer(self):
        """Clear keyboard buffer"""
        self.key_buffer.clear()
        
    def set_leds(self, scroll_lock=False, num_lock=False, caps_lock=False):
        """Set keyboard LEDs (simulated)"""
        print(f"[KEYBOARD] LEDs - Scroll: {scroll_lock}, Num: {num_lock}, Caps: {caps_lock}")
        
    def get_status(self):
        """Get keyboard status"""
        return {
            'buffer_size': len(self.key_buffer),
            'last_key': self.last_key,
            'modifiers': {
                'shift': self.shift_pressed,
                'ctrl': self.ctrl_pressed,
                'alt': self.alt_pressed
            }
        }