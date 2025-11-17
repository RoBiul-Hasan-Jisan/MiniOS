#ifndef SERIAL_H
#define SERIAL_H

#include "types.h"

// Function declarations
void serial_init(void);
int serial_received(void);
char serial_read(void);
int serial_is_transmit_empty(void);
void serial_write(char c);
void serial_writestring(const char* str);

#endif