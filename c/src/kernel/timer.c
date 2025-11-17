#include "kernel/timer.h"
#include "kernel/scheduler.h"

#define PIT_FREQUENCY 1193180
#define PIT_COMMAND 0x43
#define PIT_CHANNEL0 0x40

static uint32_t tick_count = 0;
static uint32_t frequency = 0;

void timer_callback(registers_t regs) {
    tick_count++;
    
    // Schedule next task every 10 ticks
    if(tick_count % 10 == 0) {
        schedule();
    }
}

void timer_init(uint32_t freq) {
    frequency = freq;
    
    // Register timer interrupt
    register_interrupt_handler(IRQ0, timer_callback);
    
    // Calculate divisor
    uint32_t divisor = PIT_FREQUENCY / freq;
    
    // Send command byte
    outb(PIT_COMMAND, 0x36);
    
    // Send divisor bytes
    outb(PIT_CHANNEL0, (uint8_t)(divisor & 0xFF));
    outb(PIT_CHANNEL0, (uint8_t)((divisor >> 8) & 0xFF));
    
    tick_count = 0;
}

void timer_wait(uint32_t ticks) {
    uint32_t end_ticks = tick_count + ticks;
    while(tick_count < end_ticks) {
        asm volatile("hlt");
    }
}

uint32_t timer_get_ticks(void) {
    return tick_count;
}

uint32_t timer_get_frequency(void) {
    return frequency;
}