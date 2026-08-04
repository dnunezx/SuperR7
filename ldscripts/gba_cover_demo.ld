OUTPUT_FORMAT("elf32-littlearm")
OUTPUT_ARCH(arm)
ENTRY(_start)

MEMORY {
    ROM : ORIGIN = 0x08000000, LENGTH = 32M
}

SECTIONS {
    .text : ALIGN(4) {
        *(.text)
    } > ROM
}

ASSERT(demo_boot - _start == 0xC0, "cover demo GBA header must be 192 bytes")
