#ifndef VGA_H
#define VGA_H

#include "types.h"

// VGA colors
enum vga_color {
    COLOR_BLACK = 0,
    COLOR_BLUE = 1,
    COLOR_GREEN = 2,
    COLOR_CYAN = 3,
    COLOR_RED = 4,
    COLOR_MAGENTA = 5,
    COLOR_BROWN = 6,
    COLOR_LIGHT_GREY = 7,
    COLOR_DARK_GREY = 8,
    COLOR_LIGHT_BLUE = 9,
    COLOR_LIGHT_GREEN = 10,
    COLOR_LIGHT_CYAN = 11,
    COLOR_LIGHT_RED = 12,
    COLOR_LIGHT_MAGENTA = 13,
    COLOR_LIGHT_BROWN = 14,
    COLOR_WHITE = 15,
};

// Function declarations
uint8_t vga_entry_color(enum vga_color fg, enum vga_color bg);
uint16_t vga_entry(unsigned char uc, uint8_t color);
uint16_t vga_entry_char(unsigned char uc, enum vga_color fg, enum vga_color bg);
void vga_clear_screen(uint16_t* buffer, uint8_t color);
void vga_putchar_at(uint16_t* buffer, char c, uint8_t color, size_t x, size_t y);
void vga_putchar(uint16_t* buffer, char c, uint8_t color, size_t* x, size_t* y);
void vga_writestring(uint16_t* buffer, const char* str, uint8_t color, size_t* x, size_t* y);

#endif