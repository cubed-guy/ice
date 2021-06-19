global _
segment .bss
var: resq 1
arg1: resb 1
arg2: resb 1
arg3: resb 1
arg: resq 1
dest: resq 1

segment .text
_:
mov qword dest, qword var

; dest = var.meth()
push var
call meth
add esp, 4
mov qword dest, eax

; dest = func(arg1, arg2, arg3)
push byte arg1
push byte arg2
push byte arg3
call func
add esp, 12
mov qword dest, eax

; dest = var + arg
push qword arg
push var
call __add__
add esp, 8
mov qword dest, eax
