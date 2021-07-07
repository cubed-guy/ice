extern _printf
global _main

segment .data
_p: db `%u\n`, 0

segment .bss
var: resd 1
arg: resd 1
dest: resd 1
h: resb 1
i: resb 1
sum: resb 1

segment .text
_main:

; arg = 355
mov dword [arg], 355

; 5dest = var - arg
mov eax, dword [var]
sub eax, dword [arg]
mov dword [dest], eax

; h = 9
mov byte [h], 9

; i = 246
mov byte [i], 246

; 3sum = h+i
mov  al, byte [h]
add  al, byte [i]
mov byte [sum],  al

; print(sum)
mov eax, 0
xor  al, byte [sum]
push eax
push _p
call _printf
add esp, 8

; print(dest)
mov eax, 0
xor eax, dword [dest]
push eax
push _p
call _printf
add esp, 8
