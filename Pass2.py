# This file converts source code to pseudo assembly (pasm)
# (pasm because I still have to learn assembly)
# This is pass 2 and uses data extracted during pass 1

from Pass1 import err, argv, infile
from Pass1 import data, Patterns
from re import split as re_split

outfile = open(argv[2], 'w')
p = print
def print(*args, file = outfile, **kwargs): p(*args, file = file, **kwargs)

head_label = head_func = ''
def varDict(): return data[head_label][1][head_func][1]

address_size = 64	#number of bits to store an address

size = 0
for var, meta in varDict().items():
	meta.loc = size		# right now, size refers to the current memory location

	shape = re_split(Patterns.shape_delim, meta.shape)
	dims, unit = shape[:-1], shape[-1]
	if unit[0] == '^': unit = address_size+2**int(unit[1:])
	else: unit = 2**int(unit)
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

print('.bss '+int(size))	# to allocate before execution

def get_shape(word):
	ident = Patterns.ident.match(word)
	shape = ident[1]
	if shape: return shape
	name = ident[2]
	return data[head_label][1][head_func][name][0]

for line in infile:
	pass