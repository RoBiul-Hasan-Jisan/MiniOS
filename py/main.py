#!/usr/bin/env python3
"""
MiniOS Python Simulation - Main Entry Point
"""

import os
import sys
import time
from src.boot.bootstrap import Bootloader
from src.kernel.kernel import Kernel

def main():
    """Main entry point for MiniOS simulation"""
    print("=== MiniOS Python Simulation ===")
    
    # Initialize and run bootloader
    bootloader = Bootloader()
    if not bootloader.initialize():
        print("Boot failed!")
        return 1
    
    # Create and start kernel
    kernel = Kernel()
    kernel.run()
    
    return 0

if __name__ == "__main__":
    sys.exit(main())