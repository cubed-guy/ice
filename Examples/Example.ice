-- Example Program

-- labels are a property of a variable and assignments do not transfer them

3y -- Variable initialisation. 3 -> 2^3 = 8 bits required for the variable

#3x:	-- Label header. 3 = what kind of variable can get this label
	2a(self):	-- Method header. 2 -> 2^2 = 4 bits for return value
		2out = 2	-- Init and declaration in same line (not sure if I'll keep this)
		return out

#x y	-- y now has label x

2i

i = y.a()	-- i is now 2 (uses 4 bits, so 0010)

#default y	-- inbuilt label which exists for a variable on declaration
-- now y has the default label

y.a()	-- compile error


