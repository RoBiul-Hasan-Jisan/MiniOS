import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import time
import sys
import os

class MiniOSGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("MiniOS GUI Simulation v1.0.0")
        self.root.geometry("1000x700")
        self.kernel = None
        self.os_thread = None
        self.command_queue = []  # Queue for commands
        
        self.setup_ui()
        self.start_minios()
        
    def setup_ui(self):
        # Create notebook (tabs)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Terminal Tab
        self.terminal_tab = self.create_terminal_tab()
        self.notebook.add(self.terminal_tab, text="💻 Terminal")
        
        # System Info Tab
        self.info_tab = self.create_info_tab()
        self.notebook.add(self.info_tab, text="📊 System Info")
        
    def create_terminal_tab(self):
        frame = ttk.Frame(self.notebook)
        
        # Terminal output
        self.terminal_output = scrolledtext.ScrolledText(
            frame, 
            height=25,
            width=80,
            bg='black',
            fg='white',
            font=('Courier', 10)
        )
        self.terminal_output.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.terminal_output.config(state=tk.DISABLED)
        
        # Input area
        input_frame = ttk.Frame(frame)
        input_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.terminal_input = ttk.Entry(input_frame, font=('Courier', 10))
        self.terminal_input.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        self.terminal_input.bind('<Return>', self.execute_command)
        self.terminal_input.focus()
        
        ttk.Button(input_frame, text="Send", command=self.execute_command).pack(side=tk.RIGHT)
        
        # Welcome message
        self.print_to_terminal("MiniOS GUI v1.0.0 - Terminal Ready\n")
        self.print_to_terminal("Type 'help' for available commands\n\n")
        self.print_to_terminal("user@minios:/$ ")
        
        return frame
        
    def create_info_tab(self):
        frame = ttk.Frame(self.notebook)
        
        # System status
        status_frame = ttk.LabelFrame(frame, text="System Status", padding=10)
        status_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.status_label = ttk.Label(status_frame, text="🟢 RUNNING", foreground="green")
        self.status_label.pack(anchor=tk.W)
        
        self.uptime_label = ttk.Label(status_frame, text="Uptime: 0s")
        self.uptime_label.pack(anchor=tk.W)
        
        self.process_label = ttk.Label(status_frame, text="Processes: 0")
        self.process_label.pack(anchor=tk.W)
        
        self.memory_label = ttk.Label(status_frame, text="Memory: 0 KB")
        self.memory_label.pack(anchor=tk.W)
        
        # Controls
        ttk.Button(status_frame, text="Clear Terminal", command=self.clear_terminal).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(status_frame, text="Stop OS", command=self.stop_os).pack(side=tk.LEFT)
        
        # Process list
        proc_frame = ttk.LabelFrame(frame, text="Running Processes", padding=10)
        proc_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.process_list = tk.Listbox(proc_frame, font=('Courier', 9))
        self.process_list.pack(fill=tk.BOTH, expand=True)
        
        return frame
        
    def print_to_terminal(self, text):
        """Safely print text to terminal"""
        self.terminal_output.config(state=tk.NORMAL)
        self.terminal_output.insert(tk.END, text)
        self.terminal_output.see(tk.END)
        self.terminal_output.config(state=tk.DISABLED)
        
    def start_minios(self):
        """Start MiniOS simulation"""
        def run_os():
            try:
                # Add src to path
                sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
                
                # Import and initialize MiniOS components directly
                from src.kernel.memory import MemoryManager
                from src.fs.vfs import VirtualFileSystem
                from src.kernel.scheduler import Scheduler
                
                # Initialize subsystems directly
                self.memory_manager = MemoryManager()
                self.memory_manager.initialize()
                
                self.file_system = VirtualFileSystem()
                self.file_system.initialize()
                
                self.scheduler = Scheduler()
                self.scheduler.initialize()
                
                self.start_time = time.time()
                
                # Main loop simulation
                while True:
                    # Process commands from queue
                    if self.command_queue:
                        command = self.command_queue.pop(0)
                        self.process_command(command)
                    
                    # Update UI
                    self.root.after(100, lambda: None)  # Allow UI updates
                    time.sleep(0.1)
                    
            except Exception as e:
                self.print_to_terminal(f"OS Error: {e}\n")
                
        self.os_thread = threading.Thread(target=run_os, daemon=True)
        self.os_thread.start()
        
        # Start UI updates
        self.update_ui()
        
    def update_ui(self):
        """Update UI elements"""
        try:
            # Update uptime
            if hasattr(self, 'start_time'):
                uptime = time.time() - self.start_time
                self.uptime_label.config(text=f"Uptime: {uptime:.1f}s")
            
            # Update process count
            if hasattr(self, 'scheduler'):
                proc_count = len(self.scheduler.processes) if hasattr(self.scheduler, 'processes') else 0
                self.process_label.config(text=f"Processes: {proc_count}")
                
                # Update process list
                self.process_list.delete(0, tk.END)
                if hasattr(self.scheduler, 'list_processes'):
                    processes = self.scheduler.list_processes()
                    for process in processes:
                        self.process_list.insert(tk.END, f"PID {process.pid}: {process.name}")
            
            # Update memory
            if hasattr(self, 'memory_manager'):
                if hasattr(self.memory_manager, 'get_stats'):
                    stats = self.memory_manager.get_stats()
                    mem_usage = stats.get('total_allocated', 0) // 1024
                    self.memory_label.config(text=f"Memory: {mem_usage} KB")
                    
        except Exception as e:
            print(f"UI update error: {e}")
            
        # Schedule next update
        self.root.after(1000, self.update_ui)
        
    def execute_command(self, event=None):
        """Execute terminal command"""
        command = self.terminal_input.get().strip()
        if not command:
            return
            
        # Echo the command
        self.print_to_terminal(f"{command}\n")
        self.terminal_input.delete(0, tk.END)
        
        # Add command to queue for processing
        self.command_queue.append(command)
        
    def process_command(self, command):
        """Process a command in the OS context"""
        try:
            if command == "help":
                self.show_help()
            elif command == "clear":
                self.clear_terminal()
            elif command.startswith("echo "):
                self.print_to_terminal(f"{command[5:]}\n")
            elif command == "date":
                self.print_to_terminal(f"{time.ctime()}\n")
            elif command == "ps":
                self.show_processes()
            elif command == "mem":
                self.show_memory()
            elif command == "ls":
                self.list_files()
            elif command.startswith("cat "):
                self.cat_file(command[4:])
            elif command == "exit" or command == "shutdown":
                self.stop_os()
            else:
                self.print_to_terminal(f"Command not found: {command}\n")
                
            # Show prompt after command
            self.print_to_terminal("user@minios:/$ ")
            
        except Exception as e:
            self.print_to_terminal(f"Error executing command: {e}\n")
            self.print_to_terminal("user@minios:/$ ")
        
    def show_help(self):
        """Show help in terminal"""
        help_text = """
Available commands:
  help     - Show this help
  clear    - Clear terminal
  echo     - Echo text
  date     - Show current date
  ps       - Show processes
  mem      - Show memory info
  ls       - List files
  cat      - Display file content
  exit     - Exit MiniOS
  shutdown - Shutdown MiniOS
"""
        self.print_to_terminal(help_text)
        
    def show_processes(self):
        """Show processes in terminal"""
        if hasattr(self, 'scheduler') and hasattr(self.scheduler, 'list_processes'):
            try:
                processes = self.scheduler.list_processes()
                self.print_to_terminal("PID\tName\t\tState\n")
                self.print_to_terminal("---\t----\t\t-----\n")
                for process in processes:
                    state_name = getattr(process.state, 'name', 'UNKNOWN')
                    self.print_to_terminal(f"{process.pid}\t{process.name}\t\t{state_name}\n")
            except Exception as e:
                self.print_to_terminal(f"Error showing processes: {e}\n")
        else:
            self.print_to_terminal("Process list not available\n")
                
    def show_memory(self):
        """Show memory info in terminal"""
        if hasattr(self, 'memory_manager') and hasattr(self.memory_manager, 'get_stats'):
            try:
                stats = self.memory_manager.get_stats()
                self.print_to_terminal("Memory Statistics:\n")
                self.print_to_terminal(f"  Allocations: {stats.get('allocations', 0)}\n")
                self.print_to_terminal(f"  Total: {stats.get('total_allocated', 0)} bytes\n")
            except Exception as e:
                self.print_to_terminal(f"Error showing memory: {e}\n")
        else:
            self.print_to_terminal("Memory info not available\n")
            
    def list_files(self):
        """List files in terminal"""
        if hasattr(self, 'file_system') and hasattr(self.file_system, 'list_directory'):
            try:
                files = self.file_system.list_directory("/")
                self.print_to_terminal("Files in /:\n")
                for file in files:
                    type_char = "/" if hasattr(file, 'file_type') and file.file_type.name == "DIRECTORY" else ""
                    self.print_to_terminal(f"  {file.path}{type_char}\n")
            except Exception as e:
                self.print_to_terminal(f"Error listing files: {e}\n")
        else:
            self.print_to_terminal("File system not available\n")
                
    def cat_file(self, filename):
        """Display file content in terminal"""
        if hasattr(self, 'file_system') and hasattr(self.file_system, 'read_file'):
            try:
                content = self.file_system.read_file(filename)
                if content:
                    self.print_to_terminal(f"Content of {filename}:\n")
                    self.print_to_terminal(content + "\n")
                else:
                    self.print_to_terminal(f"File not found: {filename}\n")
            except Exception as e:
                self.print_to_terminal(f"Error reading file: {e}\n")
        else:
            self.print_to_terminal(f"File system not available\n")
                
    def clear_terminal(self):
        """Clear terminal"""
        self.terminal_output.config(state=tk.NORMAL)
        self.terminal_output.delete(1.0, tk.END)
        self.terminal_output.config(state=tk.DISABLED)
        self.print_to_terminal("MiniOS GUI v1.0.0 - Terminal Ready\n")
        self.print_to_terminal("Type 'help' for available commands\n\n")
        self.print_to_terminal("user@minios:/$ ")
        
    def stop_os(self):
        """Stop MiniOS"""
        if messagebox.askyesno("Confirm", "Stop MiniOS?"):
            self.print_to_terminal("Shutting down MiniOS...\n")
            self.status_label.config(text="🔴 STOPPED", foreground="red")
            # In a real implementation, you would properly shut down the OS here

if __name__ == "__main__":
    root = tk.Tk()
    app = MiniOSGUI(root)
    root.mainloop()