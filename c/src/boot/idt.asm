[bits 32]

; IDT setup
idt_start:
    times 256 dd 0, 0
idt_end:

idt_descriptor:
    dw idt_end - idt_start - 1
    dd idt_start

; Load IDT
load_idt:
    lidt [idt_descriptor]
    ret

; Default interrupt handler
default_isr:
    pusha
    ; Handle interrupt here
    mov al, 0x20
    out 0x20, al
    popa
    iret