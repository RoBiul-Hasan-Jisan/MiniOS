#include "kernel/terminal.h"
#include "lib/string.h"

void terminal_initialize(terminal_t* terminal, uint8_t foreground, uint8_t background) {
    terminal->row = 0;
    terminal->column = 0;
    terminal->foreground = foreground;
    terminal->background = background;
    terminal->buffer = (uint16_t*)0xB8000;
    
    terminal_clear(terminal);
}

void terminal_clear(terminal_t* terminal) {
    uint16_t blank = vga_entry(' ', terminal->foreground, terminal->background);
    
    for(size_t y = 0; y < VGA_HEIGHT; y++) {
        for(size_t x = 0; x < VGA_WIDTH; x++) {
            terminal->buffer[y * VGA_WIDTH + x] = blank;
        }
    }
    
    terminal->row = 0;
    terminal->column = 0;
}

void terminal_putchar(terminal_t* terminal, char c) {
    if(c == '\n') {
        terminal->column = 0;
        if(++terminal->row == VGA_HEIGHT) {
            terminal_scroll(terminal);
        }
        return;
    }
    
    if(c == '\r') {
        terminal->column = 0;
        return;
    }
    
    if(c == '\b') {
        if(terminal->column > 0) {
            terminal->column--;
        }
        terminal_putchar(terminal, ' ');
        terminal->column--;
        return;
    }
    
    if(c == '\t') {
        terminal->column = (terminal->column + 8) & ~7;
        if(terminal->column >= VGA_WIDTH) {
            terminal->column = 0;
            if(++terminal->row == VGA_HEIGHT) {
                terminal_scroll(terminal);
            }
        }
        return;
    }
    
    uint16_t entry = vga_entry(c, terminal->foreground, terminal->background);
    terminal->buffer[terminal->row * VGA_WIDTH + terminal->column] = entry;
    
    if(++terminal->column == VGA_WIDTH) {
        terminal->column = 0;
        if(++terminal->row == VGA_HEIGHT) {
            terminal_scroll(terminal);
        }
    }
}

void terminal_writestring(terminal_t* terminal, const char* str) {
    while(*str) {
        terminal_putchar(terminal, *str++);
    }
}

void terminal_scroll(terminal_t* terminal) {
    // Move all lines up
    for(size_t y = 1; y < VGA_HEIGHT; y++) {
        for(size_t x = 0; x < VGA_WIDTH; x++) {
            terminal->buffer[(y - 1) * VGA_WIDTH + x] = terminal->buffer[y * VGA_WIDTH + x];
        }
    }
    
    // Clear last line
    uint16_t blank = vga_entry(' ', terminal->foreground, terminal->background);
    for(size_t x = 0; x < VGA_WIDTH; x++) {
        terminal->buffer[(VGA_HEIGHT - 1) * VGA_WIDTH + x] = blank;
    }
    
    terminal->row = VGA_HEIGHT - 1;
}

void terminal_setcolor(terminal_t* terminal, uint8_t foreground, uint8_t background) {
    terminal->foreground = foreground;
    terminal->background = background;
}

void terminal_getcursor(terminal_t* terminal, size_t* x, size_t* y) {
    *x = terminal->column;
    *y = terminal->row;
}

void terminal_setcursor(terminal_t* terminal, size_t x, size_t y) {
    if(x < VGA_WIDTH && y < VGA_HEIGHT) {
        terminal->column = x;
        terminal->row = y;
    }
}