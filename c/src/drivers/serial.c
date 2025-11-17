#include "drivers/serial.h"

#define SERIAL_PORT 0x3F8

void serial_init(void) {
    outb(SERIAL_PORT + 1, 0x00); // Disable interrupts
    outb(SERIAL_PORT + 3, 0x80); // Enable DLAB
    outb(SERIAL_PORT + 0, 0x03); // Set divisor to 3 (lo byte)
    outb(SERIAL_PORT + 1, 0x00); // (hi byte)
    outb(SERIAL_PORT + 3, 0x03); // 8 bits, no parity, one stop bit
    outb(SERIAL_PORT + 2, 0xC7); // Enable FIFO
    outb(SERIAL_PORT + 4, 0x0B); // IRQs enabled, RTS/DSR set
}

int serial_received(void) {
    return inb(SERIAL_PORT + 5) & 1;
}

char serial_read(void) {
    while(serial_received() == 0);
    return inb(SERIAL_PORT);
}

int serial_is_transmit_empty(void) {
    return inb(SERIAL_PORT + 5) & 0x20;
}

void serial_write(char c) {
    while(serial_is_transmit_empty() == 0);
    outb(SERIAL_PORT, c);
}

void serial_writestring(const char* str) {
    while(*str) {
        serial_write(*str++);
    }
}