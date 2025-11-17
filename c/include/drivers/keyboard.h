#ifndef KEYBOARD_H
#define KEYBOARD_H

#include "types.h"
#include "interrupt.h"

// Function declarations
void keyboard_init(void);
void keyboard_callback(registers_t regs);
char keyboard_getchar(void);
int keyboard_available(void);
void keyboard_clear_buffer(void);

#endif