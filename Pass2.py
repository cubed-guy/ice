# This file converts source code to pseudo assembly (pasm)
# (pasm because I still have to learn assembly)
# This is pass 2 and uses data extracted during pass 1

from Pass1 import Global, err, argv, infile
from Pass1 import data, Patterns

# outfile = open(argv[2], 'w')
# def output(*args, file = outfile, **kwargs): print(*args, file = file, **kwargs)
output = print

head_label = head_func = ''
def varDict(): return data[head_label][1][head_func][1]

address_size = 64	#number of bits to store an address

# Allocate memory for variables
size = 0
for var, meta in varDict().items():
	meta.loc = size		# here, size refers to the current memory location
	shape = meta.shape
	dims = Patterns.dim.findall(shape)
	unit = shape[-2:]
	if unit[0] == '^': unit = address_size+2**int(unit[1:])
	else: unit = 2**int(unit[-1])
	multiplier = 1
	isPointer = False
	for dim in dims:
		if not isPointer and dim[0] == '[': multiplier *= int(dim[1:-1])
		elif dim.isdigit(): size += 2**int(dim)
		elif dim == '*':
			if isPointer: break
			unit = address_size
			isPointer = True

	size += unit*multiplier

output('.bss', size)	# to allocate before execution

def get_shape(word):
	ident = Patterns.ident.match(word)
	shape = ident[1]
	if shape: return shape
	name = ident[2]
	return data[head_label][1][head_func][name][0]

# -----------------Keywords----------------- #
# control structures: if else elif while for
# others at the start of a line: pass return continue break global
# operators: in and or not 
# constants: True False None
# might port from py: yield async await lambda from import as
# not porting from py: is with

for line in enumerate(infile, 1):
	Global(line)
	if not Patterns.token.match(line): err('SyntaxError', 'expected token.')