[BITS 64]

; Código assembly para resgatar o RIP atual
; Autor: Helvio Junior (M4v3r1cK)
;
; Procedimento de compilação
; nasm getip64.asm -o getip64
; cat getip64 | msfvenom -p - -a x64 --platform win -e generic/none -f hex
;

_start:
    jmp call_function       ; Salta para a chamada da função

get_rip: 
    mov rax, [rsp]          ; Quando dentro da função o valor de RSP é a mesma coisa que o RIP fora da call
    ret                     ; Retorna para o fluxo normal de execução (sai da função)

call_function:
    call get_rip            ; Faz um call para a função
                            ; isso faz que o aplicativo monte a pilha para a função, fazendo com que o 
                            ; endereço do RSP (na pilha do get_rip) seja o endereço de retorno, ou seja,
                            ; o endereço do RIP do fluxo normal de execução
