# Parses basic expressions and assignments
# And now can also parse declarations

# Flags for var_encode()
GET_CLAUSE = 0b100
GET_INT = 0b010
GET_REG = 0b001

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

	vsub = re.compile(r'%\d+\b')
	rsub = re.compile(r'%\d+[a-d]\b')

def err(msg):
	print(f'File "{argv[1]}", line {line_no}')
	print('   ', line.strip())
	print(msg)
	quit(1)

def isdecl(token): return token[:1].isdigit() and not token.isdigit()

def split_type(token): return token[:1], token[1:]

def update_shapes(size, word):
	if word in variables and variables[word] != size:
		err(f'ValueError: {var!r} is already defined with a different shape')
	variables[word] = Variable(size, word)


def var_encode(var, flags = GET_CLAUSE, reg = 'a'): # flags: clause, bytes, reg
	if var not in variables: err(f'ValueError: {var!r} is not declared.')
	shape = int(variables[var].shape)
	out = ()
	if flags&GET_CLAUSE: out += (f'{size_list[shape]} [{var}]',)
	if flags&GET_INT: out += (1<<max(0, shape-3),)
	if flags&GET_REG:
		reg_temp = reg_list[shape]
		reg = reg_temp[0]+reg+reg_temp[1]
		out += (reg,)

	if len(out) == 1: return out[0]
	return out

def fun_encode(subject, op):
	# like \ in strings we'll use _ as the escape character for idents
	op = op.replace('_', ' ')

	if subject not in variables:
		if op == '  call  ': return subject.replace('_', '__')
		return op.replace(' ', '__')

	if op.startswith('  ') and op.endswith('  ') and len(op) >= 4:
		op = '_d'+op.strip()
	else: op = '_m'+op
	op = op.replace(' ', '__')

	label = variables[subject].labels[-1]
	if label[0] == '_' and label[1] != '_': label = label.replace('_', ' ', 1)
	label = label.replace('_', '__')
	label = label.replace(' ', '_')

	# print(label+op)
	return label+op

# store variable metadata (neater than using tuples)
class Variable:
	def __init__(self, shape, name):
		self.shape = shape
		self.name = name
		self.labels = []
		if len(shape) == 1: self.labels.append('_u')

	def __repr__(self):
		return f'Variable({self.shape+self.name})'
variables = {}	# formerly the `shapes` dict

indexed_sizes = 'bbbbwdq'	# byte if size <= 8, word if 16 ...
size_list = ['byte', 'byte', 'byte', 'byte', 'word', 'dword', 'qword']
reg_list  = [' l', ' l', ' l', ' l', ' x', 'ex', 'rx']

output(
	'extern _printf',
	'global _',

	'\nsegment .data',
	r'_p: db `%d\n`, 0',

	'\nsegment .bss',
sep = '\n')


# Writing to the Uninitialised Data Segment for Every Declaration line

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
			if len(decls) > 1:
				err('SyntaxError: Assignment with multiple declarations.')
			break
		elif decl:
			err('SyntaxError: Non-declaration token in declaration line.')
		else: break	# not a declaration line

	if decl:	# Output to data segment
		for size, var in decls:
			size = indexed_sizes[int(variables[var].shape)]

			# reserves one size unit with that (asm) label
			output(var+': res'+size, '1')

print('VARIABLES:', *variables.values())



# Generating Assembly Code for Every Line of Source Code

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
	'<<': '__lshift__',
	'>>': '__rshift__',
}

mfile = open('builtins.ice-snippet')
macros = {line[2:-1]: line_no for line_no, line in enumerate(mfile)
	if line.startswith('; ')}
# starts at a line starting with '; ' (mind the space)
# ends at a line with just ';' (refer builtin method part)

print('BUILT-INS:', *macros)

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
	tokens = Patterns.wsep.split(exp)
	for token in tokens:
		if not token or token.isspace(): continue

		if not isdecl(token): decl = False
		else:
			if decl: break
			else: err('SyntaxError: Cannot declare within expressions.')

		# expression lexing (might need cleaning up)
		if not subject: subject = token
		elif not op:
			token = token.strip()
			if token[0] == '(': op = '__call__'
			elif token == '.': op = False
			elif op == False: op = token
			elif token in symbols: op = symbols[token]
			elif not token: err('SyntaxError: Expected an operation.')
		elif token.isalnum(): args.append(token)

	# just assignment or no op
	if not op:
		if not dest:
			if subject: output(f'; no op {subject}')
		elif not subject: err('SyntaxError: Expected an expression.')
		elif subject.isdigit():
			dclause = var_encode(dest)
			output('\n; '+line.strip())
			output(f'mov {dclause}, {subject}')
		else:
			sclause, sreg = var_encode(subject, flags = GET_CLAUSE|GET_REG)
			dclause, dreg = var_encode(dest, flags = GET_CLAUSE|GET_REG)
			output(f'mov {sreg}, {sclause}')
			output(f'mov {dclause}, {dreg}')
		continue

	output('\n; '+line.strip())

	# builtin functions and methods
	enc_op = fun_encode(subject, op)
	if enc_op in macros:
		mfile.seek(0)

		for line in mfile.readlines()[macros[enc_op]+1:]:
			if line in (';', ';\n'): break

			# TODO: multiple subs per line
			vsub = Patterns.vsub.search(line)
			if vsub is not None:
				start, end = vsub.span()
				arg_n = int(vsub[0][1:])
				clause = var_encode(([subject]+args)[arg_n])
				line = line[:start]+clause+line[end:]

			rsub = Patterns.rsub.search(line)
			if rsub is not None:
				start, end = rsub.span()
				arg_n = int(rsub[0][1:-1])
				reg = rsub[0][-1]
				reg = var_encode(([subject]+args)[arg_n],
					flags = GET_REG, reg = reg)
				line = line[:start]+reg+line[end:]

			output(line.strip())

		if dest:
			output(f'mov {var_encode(dest)}, {var_encode(dest, flags=GET_REG)}')
		continue

	# normal function calls
	offset = 0
	for arg in args:
		arg_clause, size = var_encode(arg, flags = GET_CLAUSE|GET_INT)
		output('push', arg_clause)
		offset += size

	if op != '__call__':
		subject_clause, size = var_encode(subject, flags = GET_CLAUSE|GET_INT)
		output('push', subject_clause)
		offset += size
		output('call', enc_op)
	else: output('call', subject)
	output('add esp,', offset)

	if dest:
		output(f'mov {var_encode(dest)}, {var_encode(dest, flags=GET_REG)}')