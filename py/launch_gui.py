#!/usr/bin/env python3
"""
MiniOS GUI Launcher - Simple version
"""

import tkinter as tk
from minios_gui_tk import MiniOSGUI

def main():
    root = tk.Tk()
    app = MiniOSGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()