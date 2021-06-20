# Parses basic expressions and assignments
# And now can also parse declarations

from sys import argv
# if len(argv) <2: print('Input file not specified'); quit(1)
if len(argv)<2: argv.append('Examples/base tester.ice')
name = argv[1].rpartition('.')[0]
if len(argv)<3: argv.append(name+'.asm')

infile = open(argv[1])
out = open(argv[2], 'w')
def output(*args, file = out, **kwargs): print(*args, **kwargs, file = file)
# if len(argv)<4: argv.append(name+'.temp')

import re
class Patterns:
	# var  = re.compile(r'((?i)[a-z_]\w*\b)')
	wsep = re.compile(r'\b')

def err(msg):
	print(f'File "{argv[1]}", line {line_no}')
	print('   ', line.strip())
	print(msg)
	quit(1)

def update_shapes(size, word):
	if word in shapes and shapes[word] != size:
		err(f'ValueError: {var!r} is already defined with a different shape')
	shapes[word] = size

def with_size(var):
	if var not in shapes: err(f'ValueError: {var!r} is not declared.')
	return f'{size_list[int(shapes[var])]} [{var}]'

def isdecl(token): return token[:1].isdigit()

def split_type(token): return token[:1], token[1:]

indexed_sizes = 'bbbbwdq'	# byte for size <= 8, word = 16, double word = 32, quad ...
size_list = ['byte', 'byte', 'byte', 'byte', 'word', 'dword', 'qword']

output('global _')

# Writing to Uninitialised Data Segment for Every Declaration line

output('segment .bss')
shapes = {}
for line_no, line in enumerate(infile, 1):
	decls = []
	tokens = Patterns.wsep.split(line)[1:]

	decl = False	# we don't know if it's a declaration line yet
	for token in tokens:
		if not token or token.isspace(): continue

		if isdecl(token):
			size, var = split_type(token)
			update_shapes(size, var)
			decls.append((size, var))
			decl = True
		elif token.strip() == '=':
			if len(decls) > 1: err('SyntaxError: Assignment with multiple declarations.')
			break
		elif decl: err('SyntaxError: Non-declaration token in declaration line.')
		else: break	# not a declaration line

	if decl:	# Output to data segment
		for size, var in decls:
			size = indexed_sizes[int(shapes[var])]
			output(var+': res'+size, '1')	# reserves one size unit with that (asm) label

# (some of) python's dunder names
symbols = {
	'|' : '__or__',
	'&' : '__and__',
	'^' : '__xor__',
	'+' : '__add__',
	'-' : '__sub__',
	'*' : '__mul__',
	'/' : '__truediv__',
	'//': '__floordiv__',
	'**': '__pow__',
}


# Generating Assembly Code for Every Line of Source Code

infile.seek(0)
output('\nsegment .text')
output('_:')
for line_no, line in enumerate(infile, 1):
	decl = True
	subject = ''
	op = ''
	args = []
	dest, _, exp = line.rpartition('=')
	dest = dest.strip()
	if isdecl(dest): dest = split_type(dest)[1]
	tokens = Patterns.wsep.split(exp)[1:]	# [1:] to ignore leading non-word (for now)
	for token in tokens:
		if not token or token.isspace(): continue

		if not isdecl(token): decl = False
		else:
			if decl: break
			else: err('SyntaxError: Cannot declare within expressions.')

		if not subject: subject = token
		elif not op:
			token = token.strip()
			if token[0] == '(': op = '__call__'
			elif token == '.': op = False
			elif op == False: op = token
			elif token in symbols: op = symbols[token]
			elif not token: err('SyntaxError: Expected an operation.')
		elif token.isalnum(): args.append(token)
	
	# Output to text segment
	if not op:
		if dest: output(f'mov {with_size(dest)}, {with_size(subject)}')
		elif subject: output(f'; no op {subject}')
		continue
	output('\n; '+line.strip())
	for arg in args: output('push', with_size(arg))

	offset = len(args)*4
	if op == '__call__': output('call', subject)
	else:
		output('push', with_size(subject))
		output('call', op)
		offset += 4
	output('add esp,', offset)

	if dest: output(f'mov {with_size(dest)}, eax')	# assuming value is returned to eax

print(shapes)