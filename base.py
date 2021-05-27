# Parses basic expressions and assignments

# Basic expressions:
# var
# function(args)
# var.method(args)
# var op var

# Basic assignments just means assigning
# only to one variable at a time

from sys import argv
# if len(argv) <2: print('Input file not specified'); quit(1)
if len(argv)<2: argv.append('Examples/base tester.ice')
name = argv[1].rpartition('.')[0]
if len(argv)<3: argv.append(name+'.asm')
out = open(argv[2], 'w')
def output(*args, file = out, **kwargs): print(*args, **kwargs, file = file)
# if len(argv)<4: argv.append(name+'.temp')

# And then you'll have name+'.o' and name+'.exe'
# so many files. We'll probably have a cleanup flag
# But then we'll have to implement command-line flags,
# which isn't a priority.

import re
class Patterns:
	# var  = re.compile(r'((?i)[a-z_]\w*\b)')
	wsep = re.compile(r'\b')

def err(msg):
	print(f'File {argv[1]}, line {line_no}')
	print('   ', line.strip())
	print(msg)
	quit(1)

def update(word):
	size = int(word[0])
	word = word[1:]

	if word in shapes and shapes[word] != size:
		err('ValueError: Already defined with a different shape')
	shapes[word] = size

	return word[0]

symbols = {
	# python's dunder names
	'+' : '__add__',
	'-' : '__sub__',
	'*' : '__mul__',
	'/' : '__div__',
	'//': '__floor__',
	'**': '__pow__',
	'&' : '__and__',
	'|' : '__or__',
	'^' : '__xor__'
}

infile = open(argv[1])
shapes = {}

for line_no, line in enumerate(infile):
	subject = ''
	op = ''
	args = []
	dest, _, exp = line.rpartition('=')
	dest = dest.strip()
	tokens = Patterns.wsep.split(exp)[1:]
	for token in tokens:
		if not token or token.isspace(): continue
		if token[0].isdigit(): update(token)
		if not subject: subject = token
		elif not op:
			token = token.strip()
			if token[0] == '(': op = '__call__'
			elif token == '.': op = False
			elif op == False: op = token
			elif token in symbols: op = symbols[token]
			elif not token: err('SyntaxError: Invalid Syntax')
		elif token.isalnum(): args.append(token)
	
	# OUTPUT SECTION, WOOOO!!!
	if not op:
		if dest: output(f'mov {dest}, {subject}')
		elif subject: output(f'; no op {subject}')
		continue
	output()
	for arg in args: output('push', arg)
	output('push', subject)
	output('call', op)
	output('add esp,', len(args)*4+4)
	if dest: output(f'mov {dest}, eax')

print(shapes)