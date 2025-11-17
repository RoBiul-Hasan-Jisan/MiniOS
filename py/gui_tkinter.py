#!/usr/bin/env python3
"""
MiniOS GUI Launcher - Automatically chooses best available GUI framework
"""

import sys
import os

def main():
    # Add src to path
    sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
    
    try:
        # Try PyQt6 first
        from PyQt6.QtWidgets import QApplication
        from gui_os import MiniOSWindow
        app = QApplication(sys.argv)
        window = MiniOSWindow()
        window.show()
        sys.exit(app.exec())
        
    except ImportError:
        try:
            # Try PyQt5
            from PyQt5.QtWidgets import QApplication
            from gui_os import MiniOSWindow
            app = QApplication(sys.argv)
            window = MiniOSWindow()
            window.show()
            sys.exit(app.exec())
            
        except ImportError:
            # Fall back to Tkinter
            import tkinter as tk
            from gui_tkinter import MiniOSGUI
            root = tk.Tk()
            app = MiniOSGUI(root)
            root.mainloop()

if __name__ == "__main__":
    main()