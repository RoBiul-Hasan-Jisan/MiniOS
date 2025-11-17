#include "drivers/keyboard.h"
#include "kernel/terminal.h"

#define KEYBOARD_DATA_PORT 0x60
#define KEYBOARD_STATUS_PORT 0x64

extern terminal_t main_terminal;

static char key_buffer[256];
static int buffer_pos = 0;

// PS/2 Keyboard scancode set 1
static const char scancode_to_ascii[128] = {
    0, 27, '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '=', '\b',
    '\t', 'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', '[', ']', '\n',
    0, 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', ';', '\'', '`', 0, '\\',
    'z', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', '/', 0, '*', 0, ' ', 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
};

void keyboard_callback(registers_t regs) {
    uint8_t scancode = inb(KEYBOARD_DATA_PORT);
    
    if(scancode & 0x80) {
        // Key release
    } else {
        char c = scancode_to_ascii[scancode];
        if(c) {
            // Add to buffer
            if(buffer_pos < 255) {
                key_buffer[buffer_pos++] = c;
                key_buffer[buffer_pos] = '\0';
            }
            
            // Echo to terminal
            terminal_putchar(&main_terminal, c);
        }
    }
}

void keyboard_init(void) {
    register_interrupt_handler(IRQ1, keyboard_callback);
}

char keyboard_getchar(void) {
    while(buffer_pos == 0) {
        asm volatile("hlt");
    }
    
    char c = key_buffer[0];
    
    // Shift buffer
    for(int i = 1; i <= buffer_pos; i++) {
        key_buffer[i-1] = key_buffer[i];
    }
    buffer_pos--;
    
    return c;
}

int keyboard_available(void) {
    return buffer_pos > 0;
}

void keyboard_clear_buffer(void) {
    buffer_pos = 0;
    key_buffer[0] = '\0';
}