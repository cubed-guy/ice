extern _printf
global _

segment .data
_p: db '%d', 0

segment .bss
var: resd 1
arg: resd 1
dest: resd 1
h: resb 1
i: resb 1
sum: resb 1

segment .text
_:

; 5dest = var - arg
mov eax, dword [var]
sub eax, dword [arg]
mov dword [dest], eax

; 3sum = h+i
mov al, byte [h]
add al, byte [i]
mov byte [sum], al

; print(sum)
mov eax, 0
xor al, byte [sum]
push eax
push _p
call _printf
add esp, 8
