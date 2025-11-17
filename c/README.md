# MiniOS - A Simple Operating System

MiniOS is a simple, educational operating system written in C and assembly for x86 architecture. It demonstrates core OS concepts including boot process, memory management, multitasking, and device drivers.

## Features

- **Boot Process**: Multiboot-compliant bootloader
- **Memory Management**: Best-fit allocation with block merging
- **Multitasking**: Round-robin scheduler with priorities
- **Terminal System**: VGA text mode with scrolling
- **Shell**: Command-line interface with multiple commands
- **System Calls**: Basic system call interface
- **Drivers**: Keyboard, timer, VGA, serial
- **File System**: Virtual File System framework

## Building

### Prerequisites
```bash
# Install cross-compiler and tools
sudo apt-get install gcc-multilib grub-pc-bin qemu-system-x86