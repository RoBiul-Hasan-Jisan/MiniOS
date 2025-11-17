"""
Terminal System
"""

import sys
import threading
from src.drivers.keyboard import KeyboardDriver
from src.drivers.vga import VGADriver

class Terminal:
    def __init__(self):
        self.vga = VGADriver()
        self.keyboard = KeyboardDriver()
        self.buffer = []
        self.cursor_x = 0
        self.cursor_y = 0
        self.width = 80
        self.height = 25
        self.escape_sequence = False
        self.escape_buffer = ""
        
    def initialize(self):
        """Initialize terminal"""
        print("[TERMINAL] Initializing terminal system...")
        self.vga.initialize()
        self.keyboard.initialize()
        
        # Clear screen
        self.clear_screen()
        
        # Start keyboard input thread
        input_thread = threading.Thread(target=self._input_handler, daemon=True)
        input_thread.start()
        
    def clear_screen(self):
        """Clear terminal screen"""
        self.buffer = [[' ' for _ in range(self.width)] for _ in range(self.height)]
        self.cursor_x = 0
        self.cursor_y = 0
        self._redraw()
        
    def write_string(self, text):
        """Write string to terminal"""
        for char in text:
            self._put_char(char)
        self._redraw()
        
    def _put_char(self, char):
        """Put a character at current cursor position"""
        if char == '\n':
            self.cursor_x = 0
            self.cursor_y += 1
        elif char == '\r':
            self.cursor_x = 0
        elif char == '\t':
            self.cursor_x = (self.cursor_x + 4) & ~3
        elif char == '\b':
            if self.cursor_x > 0:
                self.cursor_x -= 1
                self.buffer[self.cursor_y][self.cursor_x] = ' '
        else:
            if self.cursor_x < self.width:
                self.buffer[self.cursor_y][self.cursor_x] = char
                self.cursor_x += 1
                
            if self.cursor_x >= self.width:
                self.cursor_x = 0
                self.cursor_y += 1
                
        # Scroll if needed
        if self.cursor_y >= self.height:
            self._scroll_up()
            self.cursor_y = self.height - 1
            
    def _scroll_up(self):
        """Scroll terminal content up"""
        for y in range(1, self.height):
            self.buffer[y-1] = self.buffer[y][:]
        self.buffer[self.height-1] = [' ' for _ in range(self.width)]
        
    def _redraw(self):
        """Redraw terminal content (simulated)"""
        # In a real terminal, this would update the physical display
        pass
        
    def _input_handler(self):
        """Handle keyboard input"""
        while True:
            key = self.keyboard.get_key()
            if key:
                self._handle_keypress(key)
                
    def _handle_keypress(self, key):
        """Handle keypress events"""
        # Simulate echo and command processing
        if key == '\r':  # Enter key
            print()  # New line
            # Process command line
            command = ''.join(self._get_current_line())
            self._process_command(command)
            # Show new prompt
            print("minios> ", end='', flush=True)
        elif key == '\x7f':  # Backspace
            print('\b \b', end='', flush=True)
        else:
            print(key, end='', flush=True)
            
    def _get_current_line(self):
        """Get current input line"""
        # Simplified - in real implementation would track input buffer
        return []
        
    def _process_command(self, command):
        """Process terminal command"""
        print(f"[TERMINAL] Command received: {command}")
        
    def set_cursor_position(self, x, y):
        """Set cursor position"""
        if 0 <= x < self.width and 0 <= y < self.height:
            self.cursor_x = x
            self.cursor_y = y
            
    def get_cursor_position(self):
        """Get cursor position"""
        return (self.cursor_x, self.cursor_y)