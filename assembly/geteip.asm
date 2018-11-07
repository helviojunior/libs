[BITS 32]

; Código assembly para resgatar o EIP atual
; Autor: Helvio Junior (M4v3r1cK)
;
; Procedimento de compilação do EggHunter
; nasm geteip.asm -o geteip -l geteip.lst
; cat geteip | msfvenom -p - -a x86 --platform win -e generic/none -f python
;

_start:
    jmp call_function       ; Salta para a chamada da função

get_eip: 
    mov eax, [esp]          ; Quando dentro da função o valor de ESP é a mesma coisa que o EIP fora da call
    ret                     ; Retorna para o fluxo normal de execução (sai da função)

call_function:
    call get_eip            ; Faz um call para a função
                            ; isso faz que o aplicativo monte a pilha para a função, fazendo com que o 
                            ; endereço do ESP (na pilha do get_eip) seja o endereço de retorno, ou seja,
                            ; o endereço do EIP do fluxo normal de execução
