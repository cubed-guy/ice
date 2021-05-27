; no op var
mov dest, var

push var
call meth
add esp, 4
mov dest, eax

push arg1
push arg2
push arg3
push func
call __call__
add esp, 16
mov dest, eax

push arg
push var
call __add__
add esp, 8
mov dest, eax
