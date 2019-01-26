[BITS 32]

; Encoder/decoder
; Autor: Helvio Junior (M4v3r1cK)
;
; Procedimento de compilação do EggHunter
; nasm decoder.asm -o decoder -l decoder.lst
; cat decoder | msfvenom -p - -a x86 --platform win -e generic/none -f hex
;
; 21 bytes encoder/decoder


_start:
    mov EAX,0x00401525      ; Salvar o endereço de início da codificação/decodificação

encode:
    XOR BYTE [EAX],0x0F     ; XOR o conteúdo de EAX com a chave 0x0F

loop_inc_one:
    inc EAX                 ; atua como um contador
                            ; incrementa 1 ao valor de EAX

loop_check:                 ; checa o endereço atual
    CMP    EAX,0x0040166E   ; Chegamos no endereço final da codificação?    
    JLE    encode           ; Se não, pulamos de volta para o XOR    

end:                        ; Colocar aqui o JMP para o shellcode
    JMP 0x00401525
    
