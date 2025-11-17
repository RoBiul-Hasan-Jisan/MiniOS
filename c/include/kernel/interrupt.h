#ifndef INTERRUPT_H
#define INTERRUPT_H

#include "types.h"

// Interrupt numbers
#define IRQ0 32
#define IRQ1 33

// Register structure
typedef struct {
    uint32_t ds;
    uint32_t edi, esi, ebp, esp, ebx, edx, ecx, eax;
    uint32_t int_no, err_code;
    uint32_t eip, cs, eflags, useresp, ss;
} registers_t;

// IDT entry
typedef struct {
    uint16_t base_low;
    uint16_t sel;
    uint8_t always0;
    uint8_t flags;
    uint16_t base_high;
} __attribute__((packed)) idt_entry_t;

// IDT pointer
typedef struct {
    uint16_t limit;
    uint32_t base;
} __attribute__((packed)) idt_ptr_t;

// ISR handler type
typedef void (*isr_t)(registers_t);

// Function declarations
void idt_init(void);
void idt_set_gate(uint8_t num, uint32_t base, uint16_t sel, uint8_t flags);
void isr_handler(registers_t regs);
void irq_handler(registers_t regs);
void register_interrupt_handler(uint8_t n, isr_t handler);

// IO port functions
uint8_t inb(uint16_t port);
void outb(uint16_t port, uint8_t val);

// Assembly functions
extern void idt_flush(uint32_t ptr);

#endif