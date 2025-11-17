#ifndef TERMINAL_H
#define TERMINAL_H

#include "types.h"
#include "drivers/vga.h"

// Terminal dimensions
#define VGA_WIDTH 80
#define VGA_HEIGHT 25

// Terminal structure
typedef struct {
    size_t row;
    size_t column;
    uint8_t foreground;
    uint8_t background;
    uint16_t* buffer;
} terminal_t;

// Function declarations
void terminal_initialize(terminal_t* terminal, uint8_t foreground, uint8_t background);
void terminal_clear(terminal_t* terminal);
void terminal_putchar(terminal_t* terminal, char c);
void terminal_writestring(terminal_t* terminal, const char* str);
void terminal_scroll(terminal_t* terminal);
void terminal_setcolor(terminal_t* terminal, uint8_t foreground, uint8_t background);
void terminal_getcursor(terminal_t* terminal, size_t* x, size_t* y);
void terminal_setcursor(terminal_t* terminal, size_t x, size_t y);

// Helper function
static inline uint16_t vga_entry(unsigned char uc, uint8_t color) {
    return (uint16_t)uc | (uint16_t)color << 8;
}

#endif