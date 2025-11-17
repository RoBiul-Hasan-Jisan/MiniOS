# MiniOS Makefile
CC = i686-elf-gcc
AS = i686-elf-as
LD = i686-elf-ld
CFLAGS = -std=gnu99 -ffreestanding -O2 -Wall -Wextra -Iinclude
ASFLAGS = -f elf
LDFLAGS = -ffreestanding -O2 -nostdlib -lgcc

# Source files
C_SOURCES = $(shell find src/ -name "*.c")
ASM_SOURCES = $(shell find src/ -name "*.asm")
OBJS = $(C_SOURCES:.c=.o) $(ASM_SOURCES:.asm=.o)

# Output files
KERNEL = minios.kernel
ISO = minios.iso

.PHONY: all clean run debug

all: $(ISO)

$(ISO): $(KERNEL)
	@mkdir -p iso/boot/grub
	cp $(KERNEL) iso/boot/
	cp scripts/grub.cfg iso/boot/grub/
	grub-mkrescue -o $(ISO) iso/

$(KERNEL): $(OBJS)
	$(CC) -T scripts/link.ld -o $@ $(LDFLAGS) $(OBJS)

%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

%.o: %.asm
	$(AS) $(ASFLAGS) $< -o $@

clean:
	rm -f $(OBJS) $(KERNEL) $(ISO)
	rm -rf iso/

run: $(ISO)
	qemu-system-i386 -cdrom $(ISO)

debug: $(ISO)
	qemu-system-i386 -cdrom $(ISO) -s -S

# Create disk image
disk: $(KERNEL)
	dd if=/dev/zero of=minos.img bs=512 count=20480
	dd if=$(KERNEL) of=minos.img conv=notrunc

.PHONY: all clean run debug disk