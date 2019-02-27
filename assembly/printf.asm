[BITS 32]

;nasm -f elf printf.asm -o teste.o
;gcc -o teste teste.o -m32

section .text
         global main
         extern printf

main:
    push ebp
    mov ebp,esp

    ; <-- Start -->
    PUSH 0x00000000
    PUSH 0x4b633172
    PUSH 0x3376344d
    PUSH ESP            ; Push stack addr 
    CALL printf
    ; <-- End -->


    add esp, 4
    mov esp,ebp
    pop ebp

    mov eax, 0
    ret
