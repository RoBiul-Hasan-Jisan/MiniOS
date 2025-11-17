#ifndef TIMER_H
#define TIMER_H

#include "types.h"
#include "interrupt.h"

// Function declarations
void timer_init(uint32_t freq);
void timer_wait(uint32_t ticks);
uint32_t timer_get_ticks(void);
uint32_t timer_get_frequency(void);

#endif