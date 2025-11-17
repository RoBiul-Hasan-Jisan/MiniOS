#include "drivers/vga.h"

uint8_t vga_entry_color(enum vga_color fg, enum vga_color bg) {
    return fg | bg << 4;
}

uint16_t vga_entry(unsigned char uc, uint8_t color) {
    return (uint16_t)uc | (uint16_t)color << 8;
}

uint16_t vga_entry_char(unsigned char uc, enum vga_color fg, enum vga_color bg) {
    return vga_entry(uc, vga_entry_color(fg, bg));
}

void vga_clear_screen(uint16_t* buffer, uint8_t color) {
    uint16_t blank = vga_entry(' ', color);
    for(size_t i = 0; i < VGA_WIDTH * VGA_HEIGHT; i++) {
        buffer[i] = blank;
    }
}

void vga_putchar_at(uint16_t* buffer, char c, uint8_t color, size_t x, size_t y) {
    buffer[y * VGA_WIDTH + x] = vga_entry(c, color);
}

void vga_putchar(uint16_t* buffer, char c, uint8_t color, size_t* x, size_t* y) {
    if(c == '\n') {
        *x = 0;
        (*y)++;
    } else if(c == '\r') {
        *x = 0;
    } else if(c == '\b') {
        if(*x > 0) {
            (*x)--;
        }
    } else if(c == '\t') {
        *x = (*x + 8) & ~7;
    } else {
        vga_putchar_at(buffer, c, color, *x, *y);
        (*x)++;
    }
    
    if(*x >= VGA_WIDTH) {
        *x = 0;
        (*y)++;
    }
    
    if(*y >= VGA_HEIGHT) {
        // Scroll screen
        for(size_t i = 0; i < (VGA_HEIGHT - 1) * VGA_WIDTH; i++) {
            buffer[i] = buffer[i + VGA_WIDTH];
        }
        
        // Clear last line
        for(size_t i = 0; i < VGA_WIDTH; i++) {
            buffer[(VGA_HEIGHT - 1) * VGA_WIDTH + i] = vga_entry(' ', color);
        }
        
        *y = VGA_HEIGHT - 1;
    }
}

void vga_writestring(uint16_t* buffer, const char* str, uint8_t color, size_t* x, size_t* y) {
    while(*str) {
        vga_putchar(buffer, *str++, color, x, y);
    }
}