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
        
        # File System Tab
        self.fs_tab = self.create_fs_tab()
        self.notebook.add(self.fs_tab, text="📁 File System")
        
        # Calculator Tab
        self.calc_tab = self.create_calc_tab()
        self.notebook.add(self.calc_tab, text="🧮 Calculator")
        
    def create_terminal_tab(self):
        frame = ttk.Frame(self.notebook)
        
        # Terminal output
        self.terminal_output = scrolledtext.ScrolledText(
            frame, 
            height=20,
            width=80,
            bg='black',
            fg='white',
            font=('Courier', 10)
        )
        self.terminal_output.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Input area
        input_frame = ttk.Frame(frame)
        input_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.terminal_input = ttk.Entry(input_frame, font=('Courier', 10))
        self.terminal_input.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        self.terminal_input.bind('<Return>', self.execute_command)
        
        ttk.Button(input_frame, text="Send", command=self.execute_command).pack(side=tk.RIGHT)
        
        # Welcome message
        self.terminal_output.insert(tk.END, "MiniOS GUI v1.0.0 - Terminal Ready\n")
        self.terminal_output.insert(tk.END, "Type 'help' for available commands\n\n")
        
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
        ttk.Button(status_frame, text="Restart OS", command=self.restart_os).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(status_frame, text="Stop OS", command=self.stop_os).pack(side=tk.LEFT)
        
        # Process list
        proc_frame = ttk.LabelFrame(frame, text="Running Processes", padding=10)
        proc_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.process_list = tk.Listbox(proc_frame, font=('Courier', 9))
        self.process_list.pack(fill=tk.BOTH, expand=True)
        
        return frame
        
    def create_fs_tab(self):
        frame = ttk.Frame(self.notebook)
        
        # File tree
        tree_frame = ttk.LabelFrame(frame, text="File System", padding=10)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.file_tree = ttk.Treeview(tree_frame, columns=('Size', 'Type'), show='tree headings')
        self.file_tree.heading('#0', text='Name')
        self.file_tree.heading('Size', text='Size')
        self.file_tree.heading('Type', text='Type')
        
        self.file_tree.pack(fill=tk.BOTH, expand=True)
        
        # File content
        content_frame = ttk.LabelFrame(frame, text="File Content", padding=10)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.file_content = scrolledtext.ScrolledText(
            content_frame,
            height=10,
            font=('Courier', 9)
        )
        self.file_content.pack(fill=tk.BOTH, expand=True)
        
        return frame
        
    def create_calc_tab(self):
        frame = ttk.Frame(self.notebook)
        
        # Calculator display
        self.calc_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.calc_var, font=('Arial', 14), 
                 justify='right', state='readonly').pack(fill=tk.X, padx=10, pady=10)
        
        # Calculator buttons
        button_frame = ttk.Frame(frame)
        button_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        buttons = [
            ['7', '8', '9', '/'],
            ['4', '5', '6', '*'],
            ['1', '2', '3', '-'],
            ['0', '.', '=', '+']
        ]
        
        for i, row in enumerate(buttons):
            for j, text in enumerate(row):
                cmd = lambda x=text: self.calc_button_click(x)
                ttk.Button(button_frame, text=text, command=cmd).grid(
                    row=i, column=j, sticky='nsew', padx=2, pady=2
                )
        
        # Control buttons
        control_frame = ttk.Frame(frame)
        control_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(control_frame, text='C', command=self.calc_clear).pack(side=tk.LEFT, padx=2)
        ttk.Button(control_frame, text='⌫', command=self.calc_backspace).pack(side=tk.LEFT, padx=2)
        
        return frame
        
    def start_minios(self):
        def run_os():
            try:
                sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
                from src.boot.bootstrap import Bootloader
                from src.kernel.kernel import Kernel
                
                bootloader = Bootloader()
                if bootloader.initialize():
                    self.kernel = Kernel()
                    self.kernel.run()
            except Exception as e:
                self.log_message(f"OS Error: {e}")
                
        self.os_thread = threading.Thread(target=run_os, daemon=True)
        self.os_thread.start()
        
        # Start UI updates
        self.update_ui()
        
    def update_ui(self):
        if self.kernel:
            # Update process count
            if hasattr(self.kernel, 'scheduler'):
                proc_count = len(self.kernel.scheduler.processes)
                self.process_label.config(text=f"Processes: {proc_count}")
                
                # Update process list
                self.process_list.delete(0, tk.END)
                processes = self.kernel.scheduler.list_processes()
                for process in processes:
                    self.process_list.insert(tk.END, f"PID {process.pid}: {process.name} ({process.state.name})")
                
            # Update memory
            if hasattr(self.kernel, 'memory_manager'):
                mem_stats = self.kernel.memory_manager.get_stats()
                mem_usage = mem_stats.get('total_allocated', 0) // 1024
                self.memory_label.config(text=f"Memory: {mem_usage} KB")
                
            # Update uptime
            if hasattr(self.kernel, 'start_time'):
                uptime = time.time() - self.kernel.start_time
                self.uptime_label.config(text=f"Uptime: {uptime:.1f}s")
                
            # Update file system
            self.update_file_tree()
            
        # Schedule next update
        self.root.after(1000, self.update_ui)
        
    def update_file_tree(self):
        if self.kernel and hasattr(self.kernel, 'file_system'):
            # Clear existing items
            for item in self.file_tree.get_children():
                self.file_tree.delete(item)
                
            # Add files
            files = self.kernel.file_system.files
            for path, file in files.items():
                name = path.split('/')[-1] or '/'
                parent = '' if path == '/' else self.find_parent(path)
                
                if file.file_type.name == 'DIRECTORY':
                    self.file_tree.insert(parent, 'end', path, text=name, values=('', 'Directory'))
                else:
                    self.file_tree.insert(parent, 'end', path, text=name, 
                                        values=(f"{file.size} bytes", file.file_type.name))
    
    def find_parent(self, path):
        # Helper to find parent in tree
        parts = path.strip('/').split('/')
        if len(parts) > 1:
            return '/'.join(parts[:-1]) or '/'
        return '/'
        
    def execute_command(self, event=None):
        command = self.terminal_input.get().strip()
        if not command:
            return
            
        self.terminal_output.insert(tk.END, f"user@minios:/$ {command}\n")
        self.terminal_input.delete(0, tk.END)
        
        # Process commands
        if command == "help":
            self.show_help()
        elif command == "clear":
            self.terminal_output.delete(1.0, tk.END)
            self.terminal_output.insert(tk.END, "MiniOS GUI v1.0.0 - Terminal Ready\n")
            self.terminal_output.insert(tk.END, "Type 'help' for available commands\n\n")
        elif command.startswith("echo "):
            self.terminal_output.insert(tk.END, command[5:] + "\n")
        elif command == "date":
            self.terminal_output.insert(tk.END, time.ctime() + "\n")
        elif command == "ps":
            self.show_processes()
        elif command == "mem":
            self.show_memory()
        elif command == "ls":
            self.list_files()
        elif command.startswith("cat "):
            self.cat_file(command[4:])
        else:
            self.terminal_output.insert(tk.END, f"Command not found: {command}\n")
            
        self.terminal_output.see(tk.END)
        
    def show_help(self):
        help_text = """
Available commands:
  help    - Show this help
  clear   - Clear terminal
  echo    - Echo text
  date    - Show current date
  ps      - Show processes
  mem     - Show memory info
  ls      - List files
  cat     - Display file content
"""
        self.terminal_output.insert(tk.END, help_text + "\n")
        
    def show_processes(self):
        if self.kernel and hasattr(self.kernel, 'scheduler'):
            processes = self.kernel.scheduler.list_processes()
            self.terminal_output.insert(tk.END, "PID\tName\t\tState\n")
            self.terminal_output.insert(tk.END, "---\t----\t\t-----\n")
            for process in processes:
                self.terminal_output.insert(tk.END, f"{process.pid}\t{process.name}\t\t{process.state.name}\n")
                
    def show_memory(self):
        if self.kernel and hasattr(self.kernel, 'memory_manager'):
            stats = self.kernel.memory_manager.get_stats()
            self.terminal_output.insert(tk.END, "Memory Statistics:\n")
            self.terminal_output.insert(tk.END, f"  Allocations: {stats['allocations']}\n")
            self.terminal_output.insert(tk.END, f"  Total: {stats['total_allocated']} bytes\n")
            
    def list_files(self):
        if self.kernel and hasattr(self.kernel, 'file_system'):
            files = self.kernel.file_system.list_directory("/")
            self.terminal_output.insert(tk.END, "Files in /:\n")
            for file in files:
                type_char = "/" if file.file_type.name == "DIRECTORY" else ""
                self.terminal_output.insert(tk.END, f"  {file.path}{type_char}\n")
                
    def cat_file(self, filename):
        if self.kernel and hasattr(self.kernel, 'file_system'):
            content = self.kernel.file_system.read_file(filename)
            if content:
                self.terminal_output.insert(tk.END, f"Content of {filename}:\n")
                self.terminal_output.insert(tk.END, content + "\n")
            else:
                self.terminal_output.insert(tk.END, f"File not found: {filename}\n")
                
    def log_message(self, message):
        print(f"[GUI] {message}")
        
    def calc_button_click(self, text):
        current = self.calc_var.get()
        if text == "=":
            try:
                result = eval(current)
                self.calc_var.set(str(result))
            except:
                self.calc_var.set("Error")
        else:
            self.calc_var.set(current + text)
            
    def calc_clear(self):
        self.calc_var.set("")
        
    def calc_backspace(self):
        current = self.calc_var.get()
        self.calc_var.set(current[:-1])
        
    def restart_os(self):
        messagebox.showinfo("Info", "Restart functionality would go here")
        
    def stop_os(self):
        if messagebox.askyesno("Confirm", "Stop MiniOS?"):
            if self.kernel:
                self.kernel.shutdown()
            self.status_label.config(text="🔴 STOPPED", foreground="red")

if __name__ == "__main__":
    root = tk.Tk()
    app = MiniOSGUI(root)
    root.mainloop()