[org 0x7C00]
[bits 16]

; Boot sector code
start:
    cli
    mov ax, 0x07C0
    mov ds, ax
    mov es, ax
    mov fs, ax
    mov gs, ax
    
    ; Set up stack
    mov ax, 0x9000
    mov ss, ax
    mov sp, 0xFFFF
    sti
    
    ; Load kernel from disk
    mov ah, 0x02        ; Read sectors
    mov al, 32          ; Sectors to read
    mov ch, 0           ; Cylinder
    mov cl, 2           ; Sector
    mov dh, 0           ; Head
    mov dl, 0x80        ; Drive
    mov bx, 0x1000      ; Load address
    int 0x13
    
    jc disk_error
    
    ; Switch to protected mode
    call switch_to_pm
    jmp $
    
disk_error:
    mov si, error_msg
    call print_string
    jmp $

print_string:
    mov ah, 0x0E
.loop:
    lodsb
    cmp al, 0
    je .done
    int 0x10
    jmp .loop
.done:
    ret

%include "src/boot/gdt.asm"

[bits 16]
switch_to_pm:
    cli
    lgdt [gdt_descriptor]
    
    mov eax, cr0
    or eax, 0x1
    mov cr0, eax
    
    jmp CODE_SEG:init_pm

[bits 32]
init_pm:
    mov ax, DATA_SEG
    mov ds, ax
    mov es, ax
    mov fs, ax
    mov gs, ax
    mov ss, ax
    
    mov ebp, 0x90000
    mov esp, ebp
    
    call 0x1000      ; Jump to kernel
    jmp $

error_msg db "Disk read error!", 0

times 510-($-$$) db 0
dw 0xAA55